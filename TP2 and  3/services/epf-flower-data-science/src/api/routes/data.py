from fastapi import APIRouter, HTTPException
import os
import json
import kaggle
import glob  # Utilisé pour rechercher des fichiers spécifiques
import shutil  # Utilisé pour renommer des fichiers
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import HTMLResponse


router = APIRouter()

DATA_FOLDER = "src/data"
JSON_FOLDER = "src/config"
DATASETS_JSON = os.path.join(JSON_FOLDER, "dataset.json")

@router.get("/download-dataset/{dataset_name}", tags=["data"])
def download_dataset(dataset_name: str):
    """
        Downloads a dataset from Kaggle and renames the CSV file.

    Description:
        This endpoint allows you to download a dataset from Kaggle based on its name,
        as defined in the `datasets.json` file. The dataset is downloaded, unzipped,
        and the main CSV file is renamed to match the given `dataset_name`.

    Inputs:
        - dataset_name (str): The name of the dataset to be downloaded. This must match
          one of the keys in the `datasets.json` file.

    Outputs:
        - Success (200): JSON object with the following keys:
            - message (str): Confirmation message of the successful download and rename.
            - path (str): File path to the renamed CSV file.
        - Error (404): Dataset not found in `datasets.json`.
        - Error (422): `datasets.json` file is invalid (e.g., malformed JSON).
        - Error (503): Service unavailable due to missing `datasets.json` or
          Kaggle dependency issues.
        - Error (500): Internal server error if processing or file handling fails.
    """
    # Ensure the data folder exists
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Load datasets.json
    try:
        with open(DATASETS_JSON, "r") as f:
            datasets = json.load(f)
    except FileNotFoundError:
        # Erreur 500 si le fichier JSON n'est pas trouvé
        raise HTTPException(status_code=503, detail="dataset.json file not found")
    except json.JSONDecodeError:
        # Erreur 500 si le fichier JSON est mal formé
        raise HTTPException(status_code=422, detail="datasets.json is not a valid JSON file")

    # Check if the dataset_name exists
    if dataset_name not in datasets:
        # Erreur 404 si le dataset_name n'existe pas dans le JSON
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{dataset_name}' not found in datasets.json"
        )

    # Get the dataset URL
    dataset_url = datasets[dataset_name]["url"]

    # Download the dataset
    try:
        kaggle.api.dataset_download_files(
            dataset_url, path=DATA_FOLDER, unzip=True
        )
    except Exception as e:
        # Erreur 500 si le téléchargement échoue
        raise HTTPException(status_code=500, detail=f"Error downloading dataset: {str(e)}")

    # Search for a CSV file in the DATA_FOLDER
    try:
        csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
        if not csv_files:
            raise FileNotFoundError("No CSV file found in the downloaded dataset.")

        # Rename the first CSV file found to match `dataset_name.csv`
        original_csv_path = csv_files[0]
        renamed_csv_path = os.path.join(DATA_FOLDER, f"{dataset_name}.csv")
        shutil.move(original_csv_path, renamed_csv_path)

        return {
            "message": f"Dataset '{dataset_name}' downloaded and renamed successfully.",
            "path": renamed_csv_path
        }
    except FileNotFoundError:
        # Erreur 500 si aucun fichier CSV n'est trouvé
        raise HTTPException(status_code=503, detail="No CSV file found in the dataset.")
    except Exception as e:
        # Erreur 500 pour toute autre erreur
        raise HTTPException(status_code=503, detail=f"Error processing dataset: {str(e)}")


@router.put("/update-dataset", tags=["data"])
def update_dataset(dataset_name: str, new_data: dict = Body(...)):
    """
    Updates or adds a dataset entry in `dataset.json`.

    Args:
        dataset_name (str): The name of the dataset to update or add.
        new_data (dict): The new data for the dataset (must include `url`).

    Returns:
        dict: Confirmation message and the updated dataset.
    """
    # Load the current datasets.json
    try:
        with open(DATASETS_JSON, "r") as f:
            datasets = json.load(f)
    except FileNotFoundError:
        datasets = {}  # If the file does not exist, start with an empty dictionary

    # Update or add the dataset
    datasets[dataset_name] = new_data

    # Save the changes back to the file
    try:
        with open(DATASETS_JSON, "w") as f:
            json.dump(datasets, f, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to dataset.json: {str(e)}")

    return {
        "message": f"Dataset '{dataset_name}' updated successfully.",
        "updated_data": {dataset_name: new_data}
    }

@router.get("/manage-datasets", response_class=HTMLResponse, tags=["data"])
def manage_datasets():
    """
    Serves an HTML form to manage datasets in `dataset.json`.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Manage Datasets</title>
    </head>
    <body>
        <h1>Manage Datasets</h1>
        <form action="/update-dataset" method="post">
            <label for="dataset_name">Dataset Name:</label><br>
            <input type="text" id="dataset_name" name="dataset_name" required><br><br>
            <label for="url">Dataset URL:</label><br>
            <input type="text" id="url" name="url" required><br><br>
            <button type="submit">Update Dataset</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
