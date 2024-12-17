from src.services.parameters import get_parameters, update_parameters
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

# Test de la récupération des paramètres
params = get_parameters()
print("Current parameters:", params)

# Test de la mise à jour des paramètres
new_params = {"param1": "new_value", "param2": "updated_value"}
update_parameters(new_params)
print("Parameters updated.")
