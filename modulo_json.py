import json
import os

ARCHIVO_ACTIVOS = "datos_activos.json"
ARCHIVO_ELIMINADOS = "datos_eliminados.json"

def cargar_json():
    """Carga los registros desde los archivos JSON en listas."""
    activos = []
    eliminados = []

    if os.path.exists(ARCHIVO_ACTIVOS):
        try:
            with open(ARCHIVO_ACTIVOS, "r", encoding="utf-8") as file:
                activos = json.load(file)
        except Exception:
            activos = []

    if os.path.exists(ARCHIVO_ELIMINADOS):
        try:
            with open(ARCHIVO_ELIMINADOS, "r", encoding="utf-8") as file:
                eliminados = json.load(file)
        except Exception:
            eliminados = []

    return activos, eliminados

def guardar_json(activos, eliminados):
    """Guarda los registros actualizados en los archivos JSON."""
    with open(ARCHIVO_ACTIVOS, "w", encoding="utf-8") as file:
        json.dump(activos, file, ensure_ascii=False, indent=4)

    with open(ARCHIVO_ELIMINADOS, "w", encoding="utf-8") as file:
        json.dump(eliminados, file, ensure_ascii=False, indent=4)
