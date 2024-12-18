import google.auth
from google.cloud import firestore
from google.oauth2 import service_account


path = "TP2_and_3/services/epf-flower-data-science/tp-mde5a-api-firebase-adminsdk-1a1dm-675ab01e07.json"

class FirestoreClient:
    """Wrapper around a database"""

    client: firestore.Client

    def __init__(self, credentials_path: str = path) -> None:
        """Init the client."""
        
        credentials = service_account.Credentials.from_service_account_file(credentials_path)

        #credentials, _ = google.auth.default()

        self.client = firestore.Client(credentials=credentials)

    def get(self, collection_name: str, document_id: str) -> dict:
        """Find one document by ID.
        Args:
            collection_name: The collection name
            document_id: The document id
        Return:
            Document value.
        """
        doc = self.client.collection(
            collection_name).document(document_id).get()
        if doc.exists:
            return doc.to_dict()
        raise FileExistsError(
            f"No document found at {collection_name} with the id {document_id}"
        )

    def add(self, collection_name: str, document_id: str, data: dict) -> dict:
        """
        Add a document to a Firestore collection.
        
        Args:
            collection_name: The collection name.
            document_id: The document ID.
            data: The data to add.
        
        Returns:
            Confirmation of the added document.
        """
        doc_ref = self.client.collection(collection_name).document(document_id)
        doc_ref.set(data)  # Creates the document or overwrites if it exists
        return {"message": f"Document {document_id} added to {collection_name}"}



    def update(self, collection_name: str, document_id: str, data: dict) -> dict:
        """
        Update a document in a Firestore collection.
        
        Args:
            collection_name: The collection name.
            document_id: The document ID.
            data: The data to update.
        
        Returns:
            Confirmation of the updated document.
        """
        doc_ref = self.client.collection(collection_name).document(document_id)
        if doc_ref.get().exists:
            doc_ref.update(data)  # Only updates existing fields
            return {"message": f"Document {document_id} updated in {collection_name}"}
        raise FileExistsError(
            f"Cannot update non-existent document {document_id} in {collection_name}"
        )