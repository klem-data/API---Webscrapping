from fastapi import APIRouter, HTTPException
import os
import json
import kaggle
import glob  # Utilisé pour rechercher des fichiers spécifiques
import shutil  # Utilisé pour renommer des fichiers
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import HTMLResponse
from fastapi import Form


router = APIRouter()

DATA_FOLDER = "src/data"
JSON_FOLDER = "src/config"
DATASETS_JSON = os.path.join(JSON_FOLDER, "dataset.json")

# Fonction pour lire le fichier JSON des datasets
def load_datasets():
    if os.path.exists(JSON_FOLDER):
        with open(DATASETS_JSON, "r") as file:
            return json.load(file)
    return {}

# Fonction pour sauvegarder le fichier JSON des datasets
def save_datasets(datasets):
    with open(DATASETS_JSON, "w") as file:
        json.dump(datasets, file, indent=4)

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

@router.get("/datasets", response_class=HTMLResponse, tags=["data"])
def show_datasets():
    """
    Affiche un tableau HTML avec les datasets disponibles.
    """
    datasets = load_datasets()

    if not datasets:
        return HTMLResponse(content="<h1>Aucun dataset disponible</h1>", status_code=404)

    # Créer un tableau HTML pour afficher les datasets
    table_content = "<table border='1' style='width:100%'><tr><th>Nom</th><th>URL</th></tr>"

    # Ajouter chaque dataset au tableau
    for dataset_key, dataset_info in datasets.items():
        table_content += f"""
        <tr>
            <td>{dataset_info['name']}</td>
            <td><a href='https://www.kaggle.com/datasets/{dataset_info['url']}' target='_blank'>{dataset_info['url']}</a></td>
        </tr>
        """

    table_content += "</table>"

    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Available Datasets</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                    border: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Datasets Disponibles</h1>
            {table_content}
            <br><br>
            <a href="/docs">Retour à la gestion </a>
        </body>
        </html>
    """, status_code=200)


@router.get("/manage-datasets", response_class=HTMLResponse, tags=["data"])
def show_manage_datasets_form():
    """
    Affiche un formulaire HTML pour entrer une URL de dataset Kaggle.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Manage Datasets</title>
    </head>
    <body>
        <h1>Download Kaggle Dataset</h1>
        <form action="/api/manage-datasets" method="post">
            <label for="dataset_name">Dataset Name:</label><br>
            <input type="text" id="dataset_name" name="dataset_name" required><br><br>
            <label for="dataset_url">Dataset URL:</label><br>
            <input type="text" id="dataset_url" name="dataset_url" required><br><br>
            <button type="submit">Add/Remove Dataset</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.post("/manage-datasets", response_class=HTMLResponse, tags=["data"])
def manage_datasets(dataset_name: str = Form(...), dataset_url: str = Form(...)):
    """
    Gère les datasets dans le fichier JSON : ajouter ou supprimer un dataset basé sur l'URL.
    
    Args:
        dataset_name (str): Le nom du dataset.
        dataset_url (str): L'URL du dataset Kaggle.
    
    Returns:
        HTMLResponse: Confirmation ou message d'erreur.
    """
    datasets = load_datasets()

    # Vérifier si le dataset existe déjà
    dataset_key = dataset_name.lower().replace(" ", "_")
    
    if dataset_key in datasets:
        # Si le dataset existe déjà, le supprimer
        del datasets[dataset_key]
        message = f"Le dataset '{dataset_name}' a été supprimé."
    else:
        # Si le dataset n'existe pas, l'ajouter
        datasets[dataset_key] = {
            "name": dataset_name,
            "url": dataset_url
        }
        message = f"Le dataset '{dataset_name}' a été ajouté avec succès."
    
    # Sauvegarde des datasets dans le fichier JSON
    save_datasets(datasets)

    # Retour à l'utilisateur avec un message de confirmation
    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h1>{message}</h1>
            <p>{message}</p>
            <a href="/api/manage-datasets">Retour au formulaire</a>
        </body>
        </html>
    """, status_code=200)