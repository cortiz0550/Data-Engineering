import os
import utils
import json


""" Here we want to start with gathering the config files """
base_path = os.getcwd()
config_path = base_path + "\\config\\quickbase_config.json"
input_path = base_path + "\\data\\processed\\"

config = utils.load_config(config_path)
config["api_key"] = "QB-User-Token " + config.get("api_key")


# Get headers and payload for request
url = config.get("base_url")
headers = {
    "Content-Type": "application/json",
    "QB-Realm-Hostname": config.get("realm"),
    "Authorization": config.get("api_key")
}

with open(input_path + "cleaned_survey_list.json", "r") as infile:
    payload = json.load(infile)

# Test api call
req = utils.make_api_request(url=url, method="POST", headers=headers, data=payload)

