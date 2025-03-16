import os
import re
import PyPDF2
import fitz  # PyMuPDF
import groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from app.domain.interfaces import Agent
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from io import BytesIO
from uuid import uuid4

# Initialize FastAPI app and router
app = FastAPI()
uploadRouter = APIRouter()

# Directory to store uploaded PDFs
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FAISS Vector Store
vector_db = {}

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@uploadRouter.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    """Allows multiple PDFs to be uploaded, stored, summarized, and indexed in FAISS."""
    responses = []

    for file in files:
        try:
            file_id = str(uuid4())  # Unique ID for the file
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

            # Save file
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            # Extract and summarize text
            text = extract_text_from_pdf(file_path)
            summary = summarize_text_with_llm(text)

            # Store summary in FAISS with file ID
            store_text_in_faiss(file_id, summary)

            responses.append({"file_id": file_id, "filename": file.filename, "summary": summary})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")

    return JSONResponse(content={"message": "Files uploaded and summarized successfully.", "files": responses})

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using PyMuPDF (fitz) with PyPDF2 as a fallback."""
    text = ""

    # Try extracting with PyMuPDF (fitz)
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text")  # Extracts text from the page
        if text.strip():  # If text was extracted, return it
            return text
    except Exception as e:
        print(f"PyMuPDF failed: {str(e)}")

    # Fallback: Try PyPDF2
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""  # Extract text if available
        return text if text.strip() else "No extractable text found."
    except Exception as e:
        print(f"PyPDF2 failed: {str(e)}")

    return "Failed to extract text from PDF."


def summarize_text_with_llm(text: str) -> str:
    """Uses LLM to summarize the extracted text."""
    client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes documents."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

def store_text_in_faiss(file_id: str, text: str):
    """Stores text in FAISS with an associated file ID."""
    global vector_db
    try:
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = text_splitter.create_documents([text])
        vector_db[file_id] = FAISS.from_documents(documents, embedding_model)
        print(f"Text from {file_id} stored in FAISS successfully.")
    except Exception as e:
        print(f"Error storing text in FAISS: {str(e)}")

@uploadRouter.get("/search")
async def search_text(query: str, file_id: str):
    """Searches for specific sections within a PDF summary using FAISS."""
    if file_id not in vector_db:
        raise HTTPException(status_code=404, detail="File not found in FAISS index.")

    retriever = vector_db[file_id].as_retriever(search_kwargs={"k": 3})
    results = retriever.get_relevant_documents(query)
    
    return JSONResponse(content={"query": query, "results": [doc.page_content for doc in results]})

@uploadRouter.get("/highlight")
async def highlight_keyword(file_id: str, keyword: str):
    """Highlights occurrences of a keyword in the summarized content."""
    if file_id not in vector_db:
        raise HTTPException(status_code=404, detail="File not found in FAISS index.")

    retriever = vector_db[file_id].as_retriever(search_kwargs={"k": 5})
    results = retriever.get_relevant_documents(keyword)

    highlighted_results = [doc.page_content.replace(keyword, f"**{keyword}**") for doc in results]

    return JSONResponse(content={"keyword": keyword, "highlighted_results": highlighted_results})

class PdfAgent(Agent):
    def __init__(self):
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    async def handle_query(self, userChatQuery: str, file_id: str) -> str:
        """Handles user queries and provides responses based on stored summaries."""
        if file_id not in vector_db:
            return "File not found in FAISS index."

        retriever = vector_db[file_id].as_retriever(search_kwargs={"k": 3})
        relevant_content = retriever.get_relevant_documents(userChatQuery)
        context = "\n".join([doc.page_content for doc in relevant_content])

        client = groq.Client(api_key=self.GROQ_API_KEY)

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers questions based on summarized PDFs."},
                {"role": "user", "content": f"Based on the PDF content, answer this: {userChatQuery}. Context: {context}"}
            ],
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

# Include router
app.include_router(uploadRouter)
