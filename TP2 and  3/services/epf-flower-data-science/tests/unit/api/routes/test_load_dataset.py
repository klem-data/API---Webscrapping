import os
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open
from src.api.routes.data import router
from src.app import get_application

app = get_application()
app.include_router(router, prefix="/data")

client = TestClient(app)

@pytest.fixture
def mock_config_file():
    config_data = {
        "iris": {
            "name": "iris",
            "url": "https://www.kaggle.com/datasets/uciml/iris"
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
        yield

@pytest.fixture
def mock_download():
    with patch("opendatasets.download") as mock_download:
        yield mock_download

def test_download_dataset_success(mock_config_file, mock_download):
    response = client.get("/data/download-dataset")
    assert response.status_code == 200
    assert response.json() == {"message": "Dataset downloaded successfully"}
    mock_download.assert_called_once_with("https://www.kaggle.com/datasets/uciml/iris", os.path.join(os.path.dirname(__file__), '../../data'))

def test_config_file_not_found():
    with patch("os.path.exists", return_value=False):
        response = client.get("/data/download-dataset")
        assert response.status_code == 404
        assert response.json() == {"detail": "Config file not found"}

def test_error_decoding_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        response = client.get("/data/download-dataset")
        assert response.status_code == 400
        assert response.json() == {"detail": "Error decoding JSON file"}

def test_dataset_url_not_found(mock_config_file):
    invalid_config_data = {
        "iris": {
            "name": "iris"
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(invalid_config_data))):
        response = client.get("/data/download-dataset")
        assert response.status_code == 400
        assert response.json() == {"detail": "Dataset URL not found in config file"}

def test_error_downloading_dataset(mock_config_file):
    with patch("opendatasets.download", side_effect=Exception("Download error")):
        response = client.get("/data/download-dataset")
        assert response.status_code == 500
        assert response.json() == {"detail": "Error downloading dataset: Download error"}