from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["project_management"]
            print("Connected to MongoDB successfully!")
        except Exception as e:
            print("MongoDB Connection Error:", e)

    def get_all_data(self):
        all_documents = []
        collections = self.db.list_collection_names()  # Get all collections

        if not collections:
            return []


        # Iterate through each collection and fetch documents
        for collection_name in collections:
            collection = self.db[collection_name]
            documents = list(collection.find())  # Fetch **all fields** in the document

            for doc in documents:
                doc["_id"] = str(doc["_id"])  # Convert ObjectId to string for compatibility
                doc["collection_name"] = collection_name  # Store collection name for metadata
                all_documents.append(doc)

        return all_documents

