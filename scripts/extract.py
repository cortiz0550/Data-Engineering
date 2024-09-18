import utils
import os
import pandas as pd


# Function to get a list of all surveys as json.
def list_surveys(config):
    url = config["survey_endpoint"]

    headers = {
        "Accept": "application/json",
        "X-API-TOKEN": config.get("api_key")
    }
    
    response = utils.make_api_request(url=url, headers=headers)
    return response


""" Here we want to start with gathering the config files """
base_path = os.getcwd()
config_path = base_path + "\\config\\qualtrics_config.json"
output_path = base_path + "\\data\\raw\\" # change this if you want to put the data somewhere else.

# Load config file.
config = utils.load_config(config_path)

# 2. Make request to survey endpoint
survey_list = pd.DataFrame(list_surveys(config=config))

# 3. Store as a csv in a datalake.
utils.store_surveys(survey_list, path=output_path, filename="survey_list.csv")
