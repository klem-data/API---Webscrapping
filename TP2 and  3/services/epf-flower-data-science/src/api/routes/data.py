import os
from fastapi import APIRouter
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

# Constants
KAGGLE_CONFIG_DIR = os.path.expanduser("~/.kaggle")
DATASET_PATH = "src/data/Iris.csv"
PROCESSED_DATASET_PATH = "src/data/processed_iris.csv"
MODEL_FILE_PATH = "src/data/random_forest_model.pkl"
ENCODER_FILE_PATH = "src/data/label_encoder.pkl"
MODEL_FILE_PATH = "src/data/random_forest_model.pkl"
ENCODER_FILE_PATH = "src/data/label_encoder.pkl"

class IrisFeatures(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float


router = APIRouter()

@router.get("/download-dataset")
async def download_dataset():
    """Downloads the Iris dataset from Kaggle."""
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files('uciml/iris', path='src/data/', unzip=True)
        return {"message": "Dataset downloaded successfully."}
    except Exception as e:
        return {"error": str(e)}

@router.get("/load-dataset")
async def load_dataset():
    """Loads the Iris dataset and returns it as JSON."""
    try:
        df = pd.read_csv(DATASET_PATH)
        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}

@router.get("/process-dataset")
async def process_dataset():
    """Processes the Iris dataset."""
    try:
        df = pd.read_csv(DATASET_PATH)
        if 'Species' not in df.columns:
            return {"error": "La colonne 'Species' n'existe pas dans le dataset."}
        if df.isnull().sum().any():
            return {"error": "Le dataset contient des valeurs manquantes."}

        label_encoder = LabelEncoder()
        df['Species'] = label_encoder.fit_transform(df['Species'])

        scaler = StandardScaler()
        df_features = df.drop(columns=['Id', 'Species'])
        X_scaled = scaler.fit_transform(df_features)
        processed_df = pd.DataFrame(X_scaled, columns=df_features.columns)

        processed_df.to_csv(PROCESSED_DATASET_PATH, index=False)
        return {
            "message": "Dataset processed successfully.",
            "example_data": processed_df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/split-dataset")
async def split_dataset():
    """Splits the Iris dataset into training and testing sets."""
    try:
        df = pd.read_csv(PROCESSED_DATASET_PATH)
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        return {
            "train": train.to_dict(orient="records"),
            "test": test.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/train-model")
async def train_model():
    """Trains the classification model using the Iris dataset."""
    try:
        df = pd.read_csv(DATASET_PATH)
        if df.empty:
            return {"error": "Le dataset est vide."}

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(df['Species'])

        processed_df = pd.read_csv(PROCESSED_DATASET_PATH)
        if processed_df.empty:
            return {"error": "Le dataset prétraité est vide."}

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(processed_df, y_encoded)

        joblib.dump(model, MODEL_FILE_PATH)
        joblib.dump(label_encoder, ENCODER_FILE_PATH)

        return {"message": "Model trained and saved successfully."}
    except Exception as e:
        return {"error": str(e)}

@router.post("/predict")
async def predict(features: IrisFeatures):
    """Makes predictions using the trained model."""
    try:
        if not os.path.exists(MODEL_FILE_PATH) or not os.path.exists(ENCODER_FILE_PATH):
            raise HTTPException(status_code=404, detail="Model or encoder file not found. Please train the model first.")

        model = joblib.load(MODEL_FILE_PATH)
        label_encoder = joblib.load(ENCODER_FILE_PATH)

        input_data = pd.DataFrame([features.dict()])
        prediction_encoded = model.predict(input_data)
        predicted_species = label_encoder.inverse_transform(prediction_encoded)

        return {"predicted_species": predicted_species[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")