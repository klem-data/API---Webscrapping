from fastapi import APIRouter
import os
import kaggle

router = APIRouter()

DATA_FOLDER = "src/data"

@router.get("/download-dataset", tags=["data"])
def download_dataset():
    """
    Downloads the Iris dataset from Kaggle and saves it to the `src/data` folder.
    """
    os.makedirs(DATA_FOLDER, exist_ok=True)
    dataset = "uciml/iris"
    try:
        kaggle.api.dataset_download_files(
            dataset, path=DATA_FOLDER, unzip=True
        )
        return {"message": "Dataset downloaded successfully.", "path": DATA_FOLDER}
    except Exception as e:
        return {"error": str(e)}
