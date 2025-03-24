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
# Ensure ChromaDB uses cosine similarity for correct distance calculations
chroma_collection = chroma_client.get_or_create_collection(
    name="project_management",  # Removed embedding_function argument
    metadata={"hnsw:space": "cosine"},
)
print("New ChromaDB collection created: project_management")


def update_embeddings(batch_size=10):
    """Fetch documents and update embeddings with proper text formatting."""
    existing_ids = (
        set(chroma_collection.get()["ids"]) if chroma_collection.count() > 0 else set()
    )
    all_documents = db.get_all_data()

    texts, ids, metadata = [], [], []

    for doc in all_documents:
        doc_id = str(doc["_id"])
        doc_metadata = flatten_dict(doc)

        # Convert metadata into natural language format
        doc_text = " ".join([f"{k}: {v}" for k, v in doc_metadata.items()])

        if doc_id not in existing_ids:
            texts.append(doc_text)
            ids.append(doc_id)
            metadata.append(doc_metadata)

        # Store data in batches
        if len(texts) >= batch_size:
            _store_batch(ids, texts, metadata)
            texts, ids, metadata = [], [], []

    if texts:  # Store any remaining data
        _store_batch(ids, texts, metadata)


def _store_batch(ids, texts, metadata):
    """Encodes text and stores embeddings in ChromaDB in batches."""
    if not ids or not texts or not metadata:
        return

    vectors = embedding_model.encode(texts).tolist()

    # Ensure metadata includes full document details
    for i in range(len(metadata)):
        metadata[i]["text"] = texts[i]  # Add full text to metadata

    # Store in ChromaDB
    chroma_collection.add(ids=ids, embeddings=vectors, metadatas=metadata)

    for i in range(len(ids)):
        print(
            f"Stored in ChromaDB: ID={ids[i]}, Metadata={json.dumps(metadata[i], indent=2)}"
        )


def flatten_dict(d, parent_key="", sep="_"):
    """Flattens nested dictionaries while preserving numeric types."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            # Preserve original type for numbers and convert others to strings
            items.append((new_key, v if isinstance(v, (int, float)) else str(v)))
    return dict(items)
