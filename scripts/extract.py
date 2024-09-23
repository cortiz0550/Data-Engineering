from scripts.utils import load_config, list_surveys, store_surveys, get_paths, remove_existing_surveys, rename_file


# Function to get a list of all surveys as json.

def extract_data():
    """ Here we want to start with gathering the config files """
    paths = get_paths()
    config_path = paths.get("base_path") + paths.get("qx_config_path")
    raw_data_path = paths.get("base_path") + paths.get("raw_data_path")

    # 1. Load config file.
    config = load_config(config_path)

    # 2. Make request to survey endpoint
    survey_list = list_surveys(config)

    # 3. Remove any existing surveys from most recent list.
    filtered_survey_list = remove_existing_surveys(raw_data_path, survey_list)

    # 4. Store master and new list as csvs in a datalake.
    store_surveys(survey_list, path=raw_data_path, filename="master_surveys_list.csv")
    store_surveys(filtered_survey_list, path=raw_data_path, filename="new_surveys_list.csv")