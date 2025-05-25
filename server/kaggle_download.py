import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
destination_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", ".kaggle"))
def download_kaggle_competition(competition_name: str="playground-series-s4e2", destination: str= destination_path, unzip: bool = True):
    """
    Downloads files from a Kaggle competition.

    Parameters:
    - competition_name: short competition identifier (e.g., 'playground-series-s4e2')
    - destination: folder where files will be saved (default is 'data')
    - unzip: whether to automatically unzip the downloaded files (default is True)
    """
    # Set environment variable to locate kaggle.json credentials

    os.environ["KAGGLE_CONFIG_DIR"] = os.path.join(os.path.expanduser("~"), ".kaggle")

    # Initialize Kaggle API client
    api = KaggleApi()
    api.authenticate()

    # Create destination directory if it doesn't exist
    os.makedirs(destination, exist_ok=True)

    # Download competition files as a ZIP archive
    print(f"Downloading competition: {competition_name}...")
    api.competition_download_files(competition_name, path=destination)
    print(f"✅ Files downloaded to ./{destination}")

    # Unzip files if requested
    if unzip:
        zip_path = os.path.join(destination, f"{competition_name}.zip")
        print(f"Unzipping {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        # Remove the zip file after extraction
        os.remove(zip_path)
        print("✅ Files unzipped successfully")

# Example usage
if __name__ == "__main__":
    print("Running Kaggle Download from main()...")
    print(f"Destination path: {destination_path}")
    download_kaggle_competition(destination = destination_path)