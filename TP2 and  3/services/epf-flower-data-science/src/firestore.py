import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

def initialize_firebase():
    """
    Initialize Firebase Admin SDK with service account credentials
    
    Returns:
        firestore.Client: Initialized Firestore client
    """
    # Chemin vers le fichier de clés de service Firebase
    cred_path = Path(__file__).parent / "config" / "serviceAccountKey.json"
    
    # Initialisation de Firebase Admin avec les credentials
    if not firebase_admin._apps:
        cred = credentials.Certificate(str(cred_path))
        firebase_admin.initialize_app(cred)
    
    # Création et retour du client Firestore
    return firestore.client()

# Création d'une instance du client Firestore
db = initialize_firebase()
