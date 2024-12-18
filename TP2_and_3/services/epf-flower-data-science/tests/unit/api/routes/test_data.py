import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from pathlib import Path
import json
import pandas as pd
from TP2_and_3.services.epf_flower_data_science.src.api.routes.data import (
    preprocess_iris_data, 
    load_iris_dataset,
    split_data, 
    train_model, 
    predict, 
    add_parameters,
    update_parameters,
    get_parameters,
    router,
)

class TestDataService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.dataset_path = Path("TP2_and_3/services/epf-flower-data-science/src/data/Iris.csv")


    def test_preprocess_iris_data(self, mock_read_csv):
        mock_df = pd.DataFrame({
            "Id": [1, 2],
            "SepalLengthCm": [5.1, 4.9],
            "SepalWidthCm": [3.5, 3.0],
            "PetalLengthCm": [1.4, 1.4],
            "PetalWidthCm": [0.2, 0.2],
            "Species": ["Iris-setosa", "Iris-virginica"],
        })
        mock_read_csv.return_value = mock_df
        X, y = preprocess_iris_data()
        self.assertEqual(X.shape, (2, 4)) 
        self.assertEqual(len(y), 2) 
        mock_read_csv.assert_called_once_with(self.dataset_path)


    def test_split_data(self):
        X, y = preprocess_iris_data()
        result = split_data()
        self.assertIn("train_data", result)
        self.assertIn("test_data", result)
        self.assertEqual(len(result["train_data"]["features"]), int(0.8 * len(X)))


    def test_train_model(self, mock_train_test_split, mock_joblib_dump):
        mock_train_test_split.return_value = ([[1], [2]], [[3], [4]], [0, 1], [0, 1])
        response = self.client.post("/train-model")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        mock_train_test_split.assert_called_once()
        mock_joblib_dump.assert_called_once()


    def test_predict(self, mock_joblib_load):
        mock_model = MagicMock()
        mock_model.predict.return_value = [0]
        mock_joblib_load.return_value = mock_model
        response = self.client.post("/predict", json={
            "SepalLengthCm": 5.1,
            "SepalWidthCm": 3.5,
            "PetalLengthCm": 1.4,
            "PetalWidthCm": 0.2
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("species", response.json())
        self.assertEqual(response.json()["species"], "Iris-setosa")


    def test_add_parameters(self, mock_add):
        mock_add.return_value = {"message": "Document added successfully."}
        response = self.client.post("/parameters/test_collection/test_doc", json={
            "data": {"param1": "test", "param2": "value"}
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Document added successfully.")


    def test_update_parameters(self, mock_update):
        mock_update.return_value = {"message": "Document updated successfully."}
        response = self.client.put("/parameters/test_collection/test_doc", json={
            "data": {"param1": "updated", "param2": "value"}
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Document updated successfully.")


    def test_get_parameters(self, mock_get):
        mock_get.return_value = {"param1": "value1", "param2": "value2"}
        response = self.client.get("/parameters/test_collection/test_doc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["param1"], "value1")
