from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from pydantic import BaseModel

router = APIRouter()
db = firestore.client()

class Parameters(BaseModel):
    n_estimators: int = 100
    criterion: str = "gini"

@router.get("/parameters")
async def get_parameters():
    """Récupère les paramètres depuis Firestore"""
    try:
        doc_ref = db.collection("parameters").document("parameters")
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(
                status_code=404,
                detail="Parameters not found in Firestore"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving parameters: {str(e)}"
        )

@router.put("/parameters")
async def update_parameters(params: Parameters):
    """Met à jour les paramètres existants dans Firestore"""
    try:
        doc_ref = db.collection("parameters").document("parameters")
        doc_ref.update({
            "n_estimators": params.n_estimators,
            "criterion": params.criterion
        })
        return {"message": "Parameters updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update parameters: {str(e)}"
        )

@router.post("/parameters")
async def add_parameters(params: Parameters):
    """Ajoute de nouveaux paramètres dans Firestore"""
    try:
        doc_ref = db.collection("parameters").document("parameters")
        doc_ref.set({
            "n_estimators": params.n_estimators,
            "criterion": params.criterion
        })
        return {"message": "Parameters added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add parameters: {str(e)}"
        )
