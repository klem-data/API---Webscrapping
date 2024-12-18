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
