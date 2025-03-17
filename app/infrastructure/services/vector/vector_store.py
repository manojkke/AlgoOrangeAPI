from .embedding_service import embedding_model, chroma_collection, update_embeddings

def retrieve_relevant_text(userChatQuery, n_results=10):
    """Retrieve the most relevant document(s) from ChromaDB based on user query."""
    if not userChatQuery:
        print("User query is empty.")
        return None

    # Ensure embeddings are updated before querying
    update_embeddings()

    query_vector = embedding_model.encode(userChatQuery).tolist()

    # Search ChromaDB for relevant documents
    results = chroma_collection.query(
        query_embeddings=[query_vector],
        n_results=n_results  # Retrieve top N results
    )

    if results and results.get("metadatas"):
        retrieved_data = results["metadatas"]  # List of metadata dicts

        # Combine all retrieved data into a readable format
        context = "\n\n".join([str(doc) for doc in retrieved_data])
        

        return context  # Return all relevant document details
    
    print("No relevant data found in ChromaDB.")
    return None
