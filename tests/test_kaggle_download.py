import os
import unittest
from unittest.mock import patch, MagicMock
from server.kaggle_download import download_kaggle_competition

class TestDownloadKaggleCompetition(unittest.TestCase):

    @patch("server.kaggle_download.KaggleApi")
    @patch("server.kaggle_download.os.makedirs")
    @patch("server.kaggle_download.zipfile.ZipFile")
    @patch("server.kaggle_download.os.remove")
    def test_download_kaggle_competition(self, mock_remove, mock_zipfile, mock_makedirs, mock_kaggle_api):
        # Mock the Kaggle API
        mock_api_instance = MagicMock()
        mock_kaggle_api.return_value = mock_api_instance

        # Mock the zipfile behavior
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

        # Define test parameters
        competition_name = "test-competition"
        destination = "/mock/destination"
        unzip = True

        # Call the function
        download_kaggle_competition(competition_name=competition_name, destination=destination, unzip=unzip)

        # Assertions
        mock_kaggle_api.assert_called_once()
        mock_api_instance.authenticate.assert_called_once()
        mock_makedirs.assert_called_once_with(destination, exist_ok=True)
        mock_api_instance.competition_download_files.assert_called_once_with(competition_name, path=destination)

        if unzip:
            zip_path = os.path.join(destination, f"{competition_name}.zip")
            mock_zipfile.assert_called_once_with(zip_path, 'r')
            mock_zip_instance.extractall.assert_called_once_with(destination)
            mock_remove.assert_called_once_with(zip_path)

    @patch("server.kaggle_download.KaggleApi")
    @patch("server.kaggle_download.os.makedirs")
    def test_download_without_unzip(self, mock_makedirs, mock_kaggle_api):
        # Mock the Kaggle API
        mock_api_instance = MagicMock()
        mock_kaggle_api.return_value = mock_api_instance

        # Define test parameters
        competition_name = "test-competition"
        destination = "/mock/destination"
        unzip = False

        # Call the function
        download_kaggle_competition(competition_name=competition_name, destination=destination, unzip=unzip)

        # Assertions
        mock_kaggle_api.assert_called_once()
        mock_api_instance.authenticate.assert_called_once()
        mock_makedirs.assert_called_once_with(destination, exist_ok=True)
        mock_api_instance.competition_download_files.assert_called_once_with(competition_name, path=destination)

if __name__ == "__main__":
    unittest.main()