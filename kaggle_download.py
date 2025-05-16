import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def descargar_competencia_kaggle(nombre_competencia: str, destino: str = ".kaggle\data", unzip: bool = True):
    """
    Descarga los archivos de una competencia de Kaggle.

    Parámetros:
    - nombre_competencia: el identificador corto de la competencia (ej. 'playground-series-s4e2')
    - destino: carpeta donde se guardarán los archivos (por defecto 'data')
    - unzip: si se desea descomprimir automáticamente los archivos (por defecto True)
    """
    # Configurar acceso a kaggle.json
    os.environ["KAGGLE_CONFIG_DIR"] = os.path.expanduser("~/.kaggle")

    # Inicializar API
    api = KaggleApi()
    api.authenticate()

    # Crear carpeta si no existe
    os.makedirs(destino, exist_ok=True)

    # Descargar archivos ZIP
    print(f"Descargando competencia: {nombre_competencia}...")
    api.competition_download_files(nombre_competencia, path=destino)
    print(f"✅ Archivos descargados en ./{destino}")

    # Descomprimir si se indica
    if unzip:
        zip_path = os.path.join(destino, f"{nombre_competencia}.zip")
        print(f"Descomprimiendo {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destino)
        os.remove(zip_path)
        print("✅ Archivos descomprimidos")

# Ejemplo de uso
if __name__ == "__main__":
    descargar_competencia_kaggle("playground-series-s4e2")
