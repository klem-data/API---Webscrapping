import os
import uvicorn
from src.app import get_application

# Set the path to kaggle.json explicitly
kaggle_json_path = os.path.join(os.path.dirname(__file__), "kaggle.json")

# Set the environment variable for the Kaggle API to the directory of kaggle.json
os.environ['KAGGLE_CONFIG_DIR'] = os.path.dirname(kaggle_json_path)

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)