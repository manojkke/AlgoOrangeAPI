import os
import fitz  # PyMuPDF
import groq
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from io import BytesIO
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from app.domain.interfaces import Agent

# Initialize FastAPI and Router
app = FastAPI()
pdfRouter = APIRouter()

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store FAISS indexes and track latest file
vector_db = {}
latest_file_id = None  # Track the latest uploaded PDF

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from a PDF file using PyMuPDF (fitz)."""
    text = ""
    try:
        doc = fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error extracting text: {str(e)}")

    return text.strip() if text else "Failed to extract text."

def store_text_in_faiss(file_id: str, text: str):
    """Stores extracted text in FAISS for retrieval."""
    global latest_file_id
    try:
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = text_splitter.create_documents([text])
        vector_db[file_id] = FAISS.from_documents(documents, embedding_model)
        latest_file_id = file_id  # Set as the latest uploaded file
        print(f"Text from {file_id} stored in FAISS successfully.")
    except Exception as e:
        print(f"Error storing text in FAISS: {str(e)}")

@pdfRouter.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF, extracts text, stores it in FAISS, and assigns a file_id."""
    try:
        file_id = str(uuid4())  # Generate a unique file ID
        pdf_bytes = await file.read()

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_bytes)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in the PDF.")

        # Store text in FAISS
        store_text_in_faiss(file_id, extracted_text)

        return JSONResponse(content={"message": "PDF uploaded and processed.", "file_id": file_id})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

class PdfAgent(Agent):
    def __init__(self):
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    async def handle_query(self, userChatQuery: str,userChatHistory: str) -> str:
        """Handles user queries and provides responses based on the latest uploaded PDF."""
        if latest_file_id is None or latest_file_id not in vector_db:
            return "No PDF found. Please upload a document first."

        retriever = vector_db[latest_file_id].as_retriever(search_kwargs={"k": 3})
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
app.include_router(pdfRouter)
 