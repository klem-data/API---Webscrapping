from pathlib import Path
from fastapi import HTTPException
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
DATA_PATH = Path("src/data")
DATASET_NAME = "iris.csv"
DATASET_PATH = DATA_PATH / DATASET_NAME


def preprocess_iris_data():
    """
    Preprocess the Iris dataset (standardize features, encode labels).
    This function returns the features and labels as arrays, not as a dictionary.
    """
    df = pd.read_csv(DATASET_PATH)
    
    X = df.drop("Species", axis=1)
    y = df["Species"]
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y_encoded
