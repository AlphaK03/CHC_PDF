import json
import os

def cargar_configuraciones(config_dir):
    config_path = os.path.join(config_dir, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def guardar_configuraciones(config, config_dir):
    config_path = os.path.join(config_dir, 'config.json')
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)

def cargar_archivos_procesados(config_dir):
    processed_files_path = os.path.join(config_dir, 'processed_files.json')
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as file:
            # Convertimos la lista almacenada en un conjunto
            return set(json.load(file))
    else:
        return set()  # Devolvemos un conjunto vacío

def guardar_archivos_procesados(processed_files, config_dir):
    processed_files_path = os.path.join(config_dir, 'processed_files.json')
    with open(processed_files_path, 'w') as file:
        # Convertimos el conjunto en una lista para almacenarlo en JSON
        json.dump(list(processed_files), file, indent=4)
