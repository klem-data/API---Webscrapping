import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred_path = Path(__file__).parent.parent / "config" / "serviceAccountKey.json"
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def get_parameters():
    """Récupère les paramètres depuis Firestore"""
    doc_ref = db.collection("parameters").document("eIxSqEg0PAg0cUAj66bh")
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def update_parameters(params: dict):
    """Met à jour les paramètres dans Firestore"""
    doc_ref = db.collection("parameters").document("eIxSqEg0PAg0cUAj66bh")
    doc_ref.set(params)
