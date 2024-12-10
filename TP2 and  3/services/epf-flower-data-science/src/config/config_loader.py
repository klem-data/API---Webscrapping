import os
import json

def load_config(env: str):
    config_path = f"./config/{env}/config.json"
    with open(config_path, "r") as f:
        return json.load(f)

current_env = os.getenv("API", "dev")
config = load_config(current_env)
print(f"Environnement actuel : {config['API']}")

