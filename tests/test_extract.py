import unittest
from unittest.mock import patch
from scripts.extract import extract_data

class TestExtractData(unittest.TestCase):

    @patch('scripts.extract.rename_file')  # Mock rename_file function
    @patch('scripts.extract.store_surveys')  # Mock store_surveys function
    @patch('scripts.extract.list_surveys')  # Mock list_surveys function
    @patch('scripts.extract.load_config')  # Mock load_config function
    @patch('scripts.extract.get_paths')  # Mock get_paths function
    def test_extract_data(self, mock_get_paths, mock_load_config, mock_list_surveys, mock_store_surveys, mock_rename_file):
        # Set up mock return values for the config and paths
        mock_get_paths.return_value = {
            "base_path": "/path/to/base/",
            "qx_config_path": "/path/to/base/config.json",
            "raw_data_path": "/path/to/raw_data/"
        }
        mock_load_config.return_value = {"api_key": "test_api_key"}
        
        # Simulate the survey list returned by list_surveys
        mock_list_surveys.return_value = [{"survey_id": "1", "name": "Survey 1"}]

        # Call the extract_data function in test mode
        extract_data(test=True)
        
        # Verify the functions were called with expected arguments
        mock_get_paths.assert_called_once()
        mock_load_config.assert_called_once_with("/path/to/base/config.json")
        mock_list_surveys.assert_called_once_with({"api_key": "test_api_key"})
        
        # Verify that store_surveys and rename_file were not called because test=True
        mock_store_surveys.assert_not_called()
        mock_rename_file.assert_not_called()


    @patch('scripts.extract.get_paths')  # Mock get_paths function
    @patch('scripts.extract.rename_file')  # Mock rename_file function
    @patch('scripts.extract.store_surveys')  # Mock store_surveys function
    @patch('scripts.extract.list_surveys')  # Mock list_surveys function
    @patch('scripts.extract.load_config')  # Mock load_config function
    def test_extract_data_without_test_flag(self, mock_load_config, mock_list_surveys, mock_store_surveys, mock_rename_file, mock_get_paths):
        # Mock the return value for get_paths without trailing slashes
        mock_get_paths.return_value = {
            "base_path": "/path/to/base",
            "qx_config_path": "/path/to/base/config.json",
            "raw_data_path": "/path/to/base/raw_data/"
        }
        
        # Set up mock return values for load_config and list_surveys
        mock_load_config.return_value = {"api_key": "test_api_key"}
        mock_list_surveys.return_value = [{"survey_id": "1", "name": "Survey 1"}]

        # Call the extract_data function without test mode
        extract_data(test=False)
        
        # Verify the functions were called with expected arguments
        mock_load_config.assert_called_once_with("/path/to/base/config.json")
        mock_list_surveys.assert_called_once_with({"api_key": "test_api_key"})
        
        mock_rename_file.assert_called_once_with("/path/to/base/raw_data/master_surveys_list.csv")
        mock_store_surveys.assert_called_once_with([{"survey_id": "1", "name": "Survey 1"}], path="/path/to/base/raw_data/", filename="master_surveys_list.csv")


if __name__ == '__main__':
    unittest.main()
