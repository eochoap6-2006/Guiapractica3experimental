import json
from pathlib import Path


ARCHIVO = Path(__file__).resolve().parent.parent / "datos" / "aerolinea.json"


def cargar_todo(archivo=ARCHIVO):
    archivo = Path(archivo)
    if not archivo.exists():
        return None
    try:
        with archivo.open(encoding="utf-8") as f:
            datos = json.load(f)
    except json.JSONDecodeError as error:
        raise ValueError("El archivo JSON no es válido. Revise los datos.") from error
    if not isinstance(datos, dict):
        raise ValueError("El archivo JSON debe contener un objeto.")
    return datos


def guardar_todo(datos, archivo=ARCHIVO):
    archivo = Path(archivo)
    archivo.parent.mkdir(parents=True, exist_ok=True)
    temporal = archivo.with_suffix(".tmp")
    with temporal.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    temporal.replace(archivo)
