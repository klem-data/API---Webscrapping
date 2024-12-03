import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import opendatasets as od
import pandas as pd
from fastapi.encoders import jsonable_encoder

from src.services.data import load_iris_dataset, process_iris_dataset, split_iris_dataset

router = APIRouter()

class DatasetInfo(BaseModel):
    name: str
    url: str

@router.get("/download-dataset")
async def download_dataset():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Vérifie si l'URL du dataset est dans le fichier JSON
    if "iris" not in config or "url" not in config["iris"]:
        raise HTTPException(status_code=400, detail="Dataset URL not found in config file")

    dataset_url = config["iris"]["url"]
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Télécharger le dataset en utilisant opendatasets
    try:
        od.download(dataset_url, data_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading dataset: {str(e)}")

    return {"message": "Dataset downloaded successfully"}

@router.get("/get-dataset-info")
async def get_dataset_info():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Vérifie si les informations du dataset sont dans le fichier JSON
    if "iris" not in config:
        raise HTTPException(status_code=400, detail="Dataset information not found in config file")

    return config["iris"]

@router.post("/add-dataset")
async def add_dataset(dataset: DatasetInfo):
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Ajoute les informations du dataset au fichier JSON
    config[dataset.name] = {"name": dataset.name, "url": dataset.url}

    # Écrit les modifications dans le fichier config.json
    try:
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to config file: {str(e)}")

    return {"message": "Dataset added successfully"}

import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import opendatasets as od

router = APIRouter()

class DatasetInfo(BaseModel):
    name: str
    url: str

@router.get("/download-dataset")
async def download_dataset():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Vérifie si l'URL du dataset est dans le fichier JSON
    if "iris" not in config or "url" not in config["iris"]:
        raise HTTPException(status_code=400, detail="Dataset URL not found in config file")

    dataset_url = config["iris"]["url"]
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Télécharger le dataset en utilisant opendatasets
    try:
        od.download(dataset_url, data_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading dataset: {str(e)}")

    return {"message": "Dataset downloaded successfully"}

@router.get("/get-dataset-info")
async def get_dataset_info():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Vérifie si les informations du dataset sont dans le fichier JSON
    if "iris" not in config:
        raise HTTPException(status_code=400, detail="Dataset information not found in config file")

    return config["iris"]

@router.post("/add-dataset")
async def add_dataset(dataset: DatasetInfo):
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Ajoute les informations du dataset au fichier JSON
    config[dataset.name] = {"name": dataset.name, "url": dataset.url}

    # Écrit les modifications dans le fichier config.json
    try:
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to config file: {str(e)}")

    return {"message": "Dataset added successfully"}

@router.put("/update-dataset")
async def update_dataset(dataset: DatasetInfo):
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')

    # Vérifie si le fichier config.json existe
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="Config file not found")

    # Lit le fichier config.json
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file")

    # Vérifie si le dataset existe dans le fichier JSON
    if dataset.name not in config:
        raise HTTPException(status_code=404, detail="Dataset not found in config file")

    # Met à jour les informations du dataset dans le fichier JSON
    config[dataset.name] = {"name": dataset.name, "url": dataset.url}

    # Écrit les modifications dans le fichier config.json
    try:
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing to config file: {str(e)}")

    return {"message": "Dataset updated successfully"}

@router.get("/load-iris-dataset")
async def load_iris_dataset_endpoint():
    try:
        df = load_iris_dataset()
    except HTTPException as e:
        raise e

    # Renvoie le dataset sous forme de JSON
    return df.to_json(orient='split')

@router.get("/process-iris-dataset")
async def process_iris_dataset_endpoint():
    try:
        df = load_iris_dataset()
        df_processed = process_iris_dataset(df)
    except HTTPException as e:
        raise e

    # Utiliser jsonable_encoder pour encoder les données avant de les renvoyer
    return jsonable_encoder(df_processed.to_dict(orient='split'))

@router.get("/split-iris-dataset")
async def split_iris_dataset_endpoint():
    try:
        df = load_iris_dataset()
        split_data = split_iris_dataset(df)
    except HTTPException as e:
        raise e

    # Renvoie les ensembles d'entraînement et de test sous forme de JSON
    return split_data