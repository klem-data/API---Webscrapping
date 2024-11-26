import os
import json
import pytest
from fastapi.testclient import TestClient
from api.routes.data import router  # Importer votre routeur
from fastapi import FastAPI

# Créez une application de test
app = FastAPI()
app.include_router(router)

client = TestClient(app)

# Dossier de test
TEST_DATA_FOLDER = "test_data"
TEST_JSON_PATH = os.path.join(TEST_DATA_FOLDER, "datasets.json")

@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Prépare l'environnement de test en créant des dossiers temporaires et des fichiers JSON.
    """
    os.makedirs(TEST_DATA_FOLDER, exist_ok=True)
    # Mock du fichier JSON
    datasets_mock = {
        "iris": {"name": "Iris Dataset", "url": "uciml/iris"},
        "titanic": {"name": "Titanic Dataset", "url": "heptapod/titanic-dataset"}
    }
    with open(TEST_JSON_PATH, "w") as f:
        json.dump(datasets_mock, f)

    yield  # Tout ce qui suit sera exécuté après les tests

    # Nettoyage
    if os.path.exists(TEST_JSON_PATH):
        os.remove(TEST_JSON_PATH)
    if os.path.exists(TEST_DATA_FOLDER):
        os.rmdir(TEST_DATA_FOLDER)


def test_download_existing_dataset(monkeypatch):
    """
    Teste le téléchargement d'un dataset existant défini dans datasets.json.
    """
    def mock_kaggle_download(*args, **kwargs):
        os.makedirs(TEST_DATA_FOLDER, exist_ok=True)
        with open(os.path.join(TEST_DATA_FOLDER, "iris_dataset.csv"), "w") as f:
            f.write("mock data")
    
    #monkeypatch.setattr("kaggle.api.dataset_download_files", mock_kaggle_download)

    response = client.get("/api/download-dataset/iris_dataset")
    assert response.status_code == 200
    assert response.json()["message"] == "Dataset 'iris' downloaded and renamed successfully."

def test_dataset_not_in_json():
    """
    Teste la réponse quand un dataset inexistant est demandé.
    """
    response = client.get("/download-dataset/unknown_dataset")
    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset 'unknown_dataset' not found in datasets.json"

def test_missing_json_file(monkeypatch):
    """
    Teste la réponse quand le fichier datasets.json est manquant.
    """
    os.remove(TEST_JSON_PATH)  # Supprime temporairement le JSON
    response = client.get("/download-dataset/iris")
    assert response.status_code == 503
    assert response.json()["detail"] == "datasets.json file not found. Server configuration issue."

def test_invalid_json_file(monkeypatch):
    """
    Teste la réponse quand le fichier datasets.json est mal formé.
    """
    with open(TEST_JSON_PATH, "w") as f:
        f.write("{invalid json}")  # Écrit un JSON invalide
    response = client.get("/download-dataset/iris")
    assert response.status_code == 422
    assert response.json()["detail"] == "datasets.json is not a valid JSON file. Fix the JSON format."

def test_no_csv_after_download(monkeypatch):
    """
    Teste la réponse quand aucun fichier CSV n'est trouvé après le téléchargement.
    """
    def mock_kaggle_download(*args, **kwargs):
        os.makedirs(TEST_DATA_FOLDER, exist_ok=True)  # Simule un dossier vide

    monkeypatch.setattr("kaggle.api.dataset_download_files", mock_kaggle_download)

    response = client.get("/download-dataset/iris")
    assert response.status_code == 500
    assert response.json()["detail"] == "No CSV file found in the dataset. This is an internal processing error."
