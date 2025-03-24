from .embedding_service import embedding_model, chroma_collection, update_embeddings
from numpy.linalg import norm


def retrieve_relevant_text(userChatQuery, n_results=10):
    """Retrieve relevant documents from ChromaDB with proper similarity search."""
    if not userChatQuery:
        print("User query is empty.")
        return None

    # Ensure embeddings are updated before querying
    update_embeddings()

    # Generate query vector and normalize it
    query_vector = embedding_model.encode(userChatQuery)
    query_vector = query_vector / norm(query_vector)  # Normalize the vector

    # Search ChromaDB for relevant documents
    results = chroma_collection.query(
        query_embeddings=[query_vector.tolist()],  # Ensure correct format
        n_results=n_results,
    )

    if results and results.get("metadatas"):
        retrieved_data = results["metadatas"]  # List of metadata dicts

        # Combine retrieved documents into readable format
        context = "\n\n".join([str(doc) for doc in retrieved_data])

        return context  # Return relevant document details

    print("No relevant data found in ChromaDB.")
    return None
