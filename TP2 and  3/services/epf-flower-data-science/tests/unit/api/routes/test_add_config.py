import os
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open
from src.api.routes.data import router, DatasetInfo
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

def test_add_dataset_success(mock_config_file):
    new_dataset = {
        "name": "air_france_reviews",
        "url": "https://www.kaggle.com/api/v1/datasets/download/saharnazyaghoobpoor/air-france-reviews-dataset"
    }
    with patch("builtins.open", mock_open()) as mocked_file:
        response = client.post("/data/add-dataset", json=new_dataset)
        assert response.status_code == 200
        assert response.json() == {"message": "Dataset added successfully"}
        
        # Vérifiez que le fichier a été ouvert en mode écriture
        mocked_file.assert_called_with(os.path.join(os.path.dirname(__file__), '../../config/config.json'), 'w')
        
        # Vérifiez que les données ont été écrites dans le fichier
        handle = mocked_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0])
        assert new_dataset["name"] in written_data
        assert written_data[new_dataset["name"]] == new_dataset

def test_config_file_not_found():
    with patch("os.path.exists", return_value=False):
        new_dataset = {
        "name": "air_france_reviews",
        "url": "https://www.kaggle.com/api/v1/datasets/download/saharnazyaghoobpoor/air-france-reviews-dataset"
        }
        response = client.post("/data/add-dataset", json=new_dataset)
        assert response.status_code == 404
        assert response.json() == {"detail": "Config file not found"}

def test_error_decoding_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        new_dataset = {
        "name": "air_france_reviews",
        "url": "https://www.kaggle.com/api/v1/datasets/download/saharnazyaghoobpoor/air-france-reviews-dataset"
        }
        response = client.post("/data/add-dataset", json=new_dataset)
        assert response.status_code == 400
        assert response.json() == {"detail": "Error decoding JSON file"}

def test_error_writing_to_config_file(mock_config_file):
    new_dataset = {
        "name": "air_france_reviews",
        "url": "https://www.kaggle.com/api/v1/datasets/download/saharnazyaghoobpoor/air-france-reviews-dataset"
    }
    with patch("builtins.open", mock_open()) as mocked_file:
        mocked_file.side_effect = Exception("Write error")
        response = client.post("/data/add-dataset", json=new_dataset)
        assert response.status_code == 500
        assert response.json() == {"detail": "Error writing to config file: Write error"}