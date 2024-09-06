import requests
import json
import os
import logging
import time

def load_config(path):
    with open(path, 'r') as json_file:
        config = json.load(json_file)
    
    for key, value in config.items():
        if isinstance(value, str) and value.startswith("QX_"):
            # Replace with the actual environment variable
            config[key] = os.getenv(value, f"{value}_not_set")

    resolved_config = {}
    for key, value in config.items():
        # Check if a value contains placeholders. Iterate if multiple.
        if isinstance(value, str) and "{" in value and "}" in value:
            previous_value = None
            while previous_value != value:
                try:
                    previous_value = value
                    value = value.format(**config)
                except KeyError as e:
                    print(f"Error resolving key {key}: missing dependency {e}")
                    break
            resolved_config[key] = value
        else:
            resolved_config[key] = value
    
    return resolved_config


# This adds an Exponential Backoff Delay to the get request when calling the API.
def make_api_request(url, headers, method="GET", data=None, max_attempts=3, timeout=30):
    base_delay = 1
    attempts = 0

    # Loop through until max attempts is reached or a successful response.
    while attempts < max_attempts:
        try:
            surveys = []
            while url is not None:
                response = requests.request(method=method, url=url, headers=headers, json=data, timeout=timeout)
                response.raise_for_status()
                response_json = response.json()
                url = response_json["result"]["nextPage"]
                surveys.extend(response_json["result"]["elements"])
            break
        except Exception as e:
            logging.error(f"Request failed on attempt {attempts}: {e}")
            attempts += 1

            delay = base_delay * (2 ** attempts)
            time.sleep(delay)
        
    else:
        raise

    return surveys


# Store surveys 
def store_surveys(survey_list, path):
    survey_list.to_csv(path + "survey_list.csv", index=False)
    print("Surveys downloaded.")