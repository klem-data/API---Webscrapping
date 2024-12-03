import os
import pandas as pd
from fastapi import HTTPException
from sklearn.model_selection import train_test_split


def load_iris_dataset() -> pd.DataFrame:
    data_dir = os.path.join(os.path.dirname(__file__), '../data/iris')
    dataset_path = os.path.join(data_dir, 'Iris.csv')

    # Vérifie si le fichier du dataset existe
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail="Dataset file not found")

    # Charge le dataset
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading dataset: {str(e)}")

    return df

def process_iris_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # Renommer les colonnes contenant "iris"
    try:
        df_processed = df.rename(columns=lambda x: x.replace('iris-', ''))
        # Enlever "iris-" dans les noms des espèces
        df_processed['Species'] = df_processed['Species'].str.replace('iris-', '', case=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")

    return df_processed

def split_iris_dataset(df: pd.DataFrame) -> dict:
    try:
        X = df.drop(columns=['Species'])
        y = df['Species']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")

    return {
        "X_train": X_train.to_json(orient='split'),
        "X_test": X_test.to_json(orient='split'),
        "y_train": y_train.to_json(orient='split'),
        "y_test": y_test.to_json(orient='split')
    }