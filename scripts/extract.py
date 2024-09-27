from scripts.utils import load_config, list_surveys, store_surveys, get_paths, rename_file

# I need to add funtionality to get all users surveys. 
# This will look like calling the list surveys endpoint and gathering users
# Then calling the api endpoint for each user to then call the list survey endpoint for them.
# Append all these surveys to master file.

def extract_data(test=False):
    """ Here we want to start with gathering the config files """
    paths = get_paths()
    config_path = paths.get("qx_config_path")
    raw_data_path = paths.get("raw_data_path")

    filename = "master_surveys_list.csv"

    # 1. Load config file.
    config = load_config(config_path)

    # 2. Make request to survey endpoint
    survey_list = list_surveys(config)

    if not test:
        # 3. Rename old master list and store new master list as csv in a datalake.
        rename_file(raw_data_path + filename)
        store_surveys(survey_list, path=raw_data_path, filename=filename)