from scripts.utils import load_config, list_surveys, store_surveys, get_paths, remove_existing_surveys, rename_file


# Function to get a list of all surveys as json.

def extract_data():
    """ Here we want to start with gathering the config files """
    paths = get_paths()
    config_path = paths.get("base_path") + paths.get("qx_config_path")
    raw_data_path = paths.get("base_path") + paths.get("raw_data_path")

    filename = "master_surveys_list.csv"

    # 1. Load config file.
    config = load_config(config_path)

    # 2. Make request to survey endpoint
    survey_list = list_surveys(config)

    # 4. Rename old master list and store new master list as csv in a datalake.
    rename_file(raw_data_path + filename)
    store_surveys(survey_list, path=raw_data_path, filename=filename)