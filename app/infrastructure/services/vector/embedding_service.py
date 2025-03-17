import chromadb
from sentence_transformers import SentenceTransformer
from app.infrastructure.db.mongo_db import MongoDB
import json

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize MongoDB
db = MongoDB()

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection(name="project_management")


def update_embeddings(batch_size=10):
    """Fetch all documents from MongoDB and update ChromaDB embeddings."""
    # Get existing document IDs from ChromaDB
    existing_ids = set(chroma_collection.get()["ids"]) if chroma_collection.count() > 0 else set()
    print("Existing IDs in ChromaDB:", existing_ids)  # Debugging

    # Fetch all documents from MongoDB
    all_documents = db.get_all_data()
    print("Fetched documents from MongoDB:", all_documents)  # Debugging

    if not all_documents:
        print("No documents found in MongoDB.")
        return

    texts, ids, metadata = [], [], []

    for doc in all_documents:
        doc_id = str(doc["_id"])
        print("Processing document ID:", doc_id)  # Debugging

        # Convert nested fields properly
        doc_metadata = flatten_dict(doc)
        print("Flattened Metadata:", doc_metadata)  # Debugging

        # Convert all document fields into a single text string
        try:
            doc_text = json.dumps(doc_metadata)  # Convert to JSON format
        except (TypeError, ValueError) as e:
            print(f"Error encoding document ID {doc_id} to JSON: {e}")
            continue
        print("Document Text:", doc_text)  # Debugging

        if doc_id not in existing_ids:
            texts.append(doc_text)
            ids.append(doc_id)
            metadata.append(doc_metadata)  # Store full document metadata
        else:
            print(f"Document ID {doc_id} already exists in ChromaDB. Skipping.")

        # Ensure batch storage
        if len(texts) >= batch_size:
            print("Batch ready for storage:", ids, texts, metadata)  # Debugging
            _store_batch(ids, texts, metadata)
            texts, ids, metadata = [], [], []  # Reset batch lists

    # Store remaining documents if any
    if texts:
        print("Storing remaining batch:", ids, texts, metadata)  # Debugging
        _store_batch(ids, texts, metadata)

    print(f"Stored {len(all_documents)} total embeddings in ChromaDB!")

def _store_batch(ids, texts, metadata):
    """Encodes text and stores embeddings in ChromaDB in batches."""
    if not ids or not texts or not metadata:
        print("Skipping batch: No data to store.")
        return
    
    vectors = embedding_model.encode(texts).tolist()

    # Ensure metadata includes full document details
    for i in range(len(metadata)):
        metadata[i]["text"] = texts[i]  # Add full text to metadata
    
    # Store in ChromaDB
    chroma_collection.add(ids=ids, embeddings=vectors, metadatas=metadata)

    # Debugging: Print stored metadata
    print(f"Stored {len(ids)} embeddings in ChromaDB.")
    for i in range(len(ids)):
        print(f"Stored in ChromaDB: ID={ids[i]}, Metadata={json.dumps(metadata[i], indent=2)}")

def flatten_dict(d, parent_key='', sep='_'):
    """Flattens nested dictionaries into a single-level dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, str(v)))
    return dict(items)
