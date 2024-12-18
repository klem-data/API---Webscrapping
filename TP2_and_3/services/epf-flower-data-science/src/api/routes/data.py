from fastapi import APIRouter, HTTPException
from pathlib import Path
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.services.data import preprocess_iris_data
from sklearn.linear_model import LogisticRegression
import joblib
import json
from pydantic import BaseModel
from firestore_client import FirestoreClient


router = APIRouter()
firestore_client = FirestoreClient()


DATA_PATH = Path("TP2_and_3/services/epf-flower-data-science/src/data")
DATASET_NAME = "Iris.csv"
DATASET_PATH = DATA_PATH / DATASET_NAME
KAGGLE_CREDENTIALS = Path("src/config/kaggle.json")

MODEL_PATH = Path("src/models")
MODEL_NAME = "logistic_regression_model.pkl"
MODEL_FILE = MODEL_PATH / MODEL_NAME

SPECIES_MAPPING = {
    0: "Iris-setosa",
    1: "Iris-versicolor",
    2: "Iris-virginica"
}

with open("TP2_and_3/services/epf-flower-data-science/src/config/model_parameters.json", "r") as file:
    model_params = json.load(file)["LogisticRegression"]

class IrisInput(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

@router.get("/datasets/{name}", tags=["Datasets"])
async def download_dataset(name: str):
    """
    Download a dataset from Kaggle using kagglehub and store it in the src/data directory.
    The name parameter should match Kaggle's dataset identifier (e.g., uciml/iris).
    """
    if not KAGGLE_CREDENTIALS.is_file():
        raise HTTPException(
            status_code=500,
            detail=f"Kaggle credentials not found. Place kaggle.json at {KAGGLE_CREDENTIALS}."
        )
    
    os.environ["KAGGLE_CONFIG_DIR"] = str(KAGGLE_CREDENTIALS.parent)
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    try:
        dataset_path = kaggle.dataset_download(name, path=str(DATA_PATH))
        return {
            "message": f"Dataset '{name}' downloaded successfully.",
            "files": [str(file) for file in dataset_path.iterdir()]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download dataset: {str(e)}"
        )

@router.get("/load-iris-data", tags=["Datasets"], summary="Load Iris Dataset", description="Loads the Iris dataset as a JSON response.")
async def load_iris_dataset():
    """
    Load the Iris dataset as a pandas DataFrame and return it as a JSON response.
    """
    # Check if the Iris dataset file exists
    if not DATASET_PATH.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{DATASET_NAME}' not found. Please download it first."
        )

    try:
        df = pd.read_csv(DATASET_PATH)
        return df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries (JSON format)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading dataset: {str(e)}"
        )


@router.get("/split-iris-data", tags=["Datasets"])
def split_data(test_size: float = 0.2, random_state: int = 42):
    """
    Split the preprocessed dataset into training and testing sets.
    Returns the train-test split data in a dictionary format.
    """
    try:
        X, y = preprocess_iris_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return {
            "train_data": {
                "features": X_train.tolist(),
                "labels": y_train.tolist()
            },
            "test_data": {
                "features": X_test.tolist(),
                "labels": y_test.tolist()
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during data splitting: {str(e)}"
        )
    

@router.post("/train-model", tags=["Model"])
def train_model():
    """
    Train a classification model with the preprocessed Iris dataset and save it to the src/models folder.
    """
    try:
        split_result = split_data()
        X_train = split_result["train_data"]["features"]
        y_train = split_result["train_data"]["labels"]

        model = LogisticRegression(**model_params)
        model.fit(X_train, y_train)
        MODEL_PATH.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        joblib.dump(model, MODEL_FILE)

        return {"message": "Model trained and saved successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error training the model: {str(e)}"
        )

@router.post("/predict", tags=["Model"])
def predict(input_data: IrisInput):
    """
    Make a prediction using the trained logistic regression model.
    """
    try:
        print("Received input data:", input_data)  # Log received data
        
        # Check if the model exists
        if not MODEL_FILE.is_file():
            raise HTTPException(
                status_code=404,
                detail="Model not found. Please train the model first."
            )
        print("Model file exists at:", MODEL_FILE)  # Log model path

        # Load the trained model
        model = joblib.load(MODEL_FILE)
        print("Model loaded successfully.")  # Log model loading status

        input_array = pd.DataFrame([input_data.dict()])
        print("Input array prepared:", input_array)

        prediction = model.predict(input_array)
        predicted_class = int(prediction[0])  # Get the predicted class (integer)
        predicted_species = SPECIES_MAPPING.get(predicted_class, "Unknown")  # Map to species name
        print("Prediction result:", predicted_class, predicted_species)  # Log prediction result

        return {
            "prediction": predicted_class,
            "species": predicted_species
        }


    except FileNotFoundError as e:
        print("File not found error:", str(e))
        raise HTTPException(status_code=404, detail="Model file not found.")

    except ValueError as e:
        print("Value error during prediction:", str(e))
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

    except Exception as e:
        print("General error during prediction:", str(e))
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")


@router.get("/parameters/{collection_name}/{document_id}")
async def get_parameters(collection_name: str, document_id: str):
    try:
        parameters = firestore_client.get(collection_name, document_id)
        return parameters
    except FileExistsError as e:
        raise HTTPException(status_code=404, detail=str(e))
