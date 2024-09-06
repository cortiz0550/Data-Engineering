import utils
import os
import pandas as pd

""" Here we want to start with gathering the config files """
base_path = os.getcwd()
config_path = base_path + "\\config\\qualtrics_config.json"
config = utils.load_config(config_path)


# Function to get a list of all surveys as json.
def list_surveys(config):
    url = config["survey_endpoint"]

    headers = {
        "Accept": "application/json",
        "X-API-TOKEN": config["api_key"]
    }
    
    response = utils.make_api_request(url=url, headers=headers)
    return response

# 2. Make request to survey endpoint
survey_list = pd.DataFrame(list_surveys(config=config))



# 3. Store as a csv in a datalake.
output_folder = base_path + "\\Data\\"
survey_list.to_csv(output_folder + "survey_list.csv", index=False)
print("Surveys downloaded.")
