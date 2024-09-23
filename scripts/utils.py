from datetime import date
import requests
import json
import os
import logging
import time
import pandas as pd

""" General functions """
# This gets the paths for the whole pipeline.
def get_paths():

    paths = {
        "base_path": os.getcwd(),
        "qx_config_path": "\\config\\qualtrics_config.json",
        "qb_config_path": "\\config\\quickbase_config.json",
        "raw_data_path": "\\data\\raw\\", # change this if you want to put the data somewhere else.
        "processed_data_path": "\\data\\processed\\" # change this if you want to put the data somewhere else.
    }

    return paths

def load_config(path):
    with open(path, 'r') as json_file:
        config = json.load(json_file)
    
    for key, value in config.items():
        # Environment variables for this start with QX or QB
        if isinstance(value, str) and (value.startswith("QX_") or value.startswith("QB_")):
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

def rename_file(path):

    updated_path = path.replace("current_survey_list", "survey_list")
    filename = updated_path.split(".")
    filename.insert(len(filename) - 1, "_" + str(date.today()))
    new_filename = "".join(filename[:-1]) + "." + filename[-1]

    try:
        os.replace(path, new_filename)
    except FileNotFoundError:
        print("Creating new survey list file.")

# This adds an Exponential Backoff Delay to the get request when calling the API.
def make_api_request(url, headers, method="GET", data=None, max_attempts=3, timeout=30):
    base_delay = 1
    attempts = 0

    # Run this for GET requests (survey listing)
    if method == "GET":
        # Loop through until max attempts is reached or a successful response.
        while attempts < max_attempts:
            try:
                surveys = []

                # This loops through until all surveys are gathered.
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

    # Run this for POST requests
    else:
        try:
            req = requests.request(method=method, url=url, headers=headers, json=data, timeout=timeout)
            while req.status_code != 200 and attempts < max_attempts:
                print(f"Error: {req.status_code}")
                print(req.json())
                attempts += 1
                req = requests.request(method=method, url=url, headers=headers, json=data, timeout=timeout)
            else:
                print("Surveys uploaded to Quickbase successfully.")
        except Exception as e:
            logging.error(f"Request failed: {e}")
            print(e)
    
        return None

def store_surveys(survey_list, path, filename="current_survey_list.csv"):
    filename_breakdown = filename.split(".")
    ext = filename_breakdown[-1]

    if ext == "csv":
        survey_list.to_csv(path + filename, index=False)
    else:
        with open(path + filename, "w") as outfile:
            json.dump(survey_list, outfile, indent=4)
    print(f"{filename} successfully stored.")


""" Extract functions """
def list_surveys(config):
    url = config["survey_endpoint"]

    headers = {
        "Accept": "application/json",
        "X-API-TOKEN": config.get("api_key")
    }
    
    response = make_api_request(url=url, headers=headers)
    return pd.DataFrame(response)

# Remove any surveys we have already recieved and that the status has not changed for.
def remove_existing_surveys(raw_data_path, survey_list):

    try:
        existing_surveys = pd.read_csv(raw_data_path + "current_survey_list.csv")
    except FileNotFoundError:
        return survey_list

    # Left merge gets only the rows in the most recent survey list
    all_surveys_df = survey_list.merge(existing_surveys.drop_duplicates(), on=list(survey_list.columns), how="left", indicator=True)
    all_surveys_df = all_surveys_df[all_surveys_df["_merge"] == "left_only"]
    all_surveys_df = all_surveys_df.drop(["_merge"], axis=1)
    
    return all_surveys_df


""" Transform functions"""
def get_file(path):
    ext = path.split(".")[-1]
    if ext == "csv":
        df = pd.read_csv(path)
    elif ext == "json":
        df = pd.read_json(path)
    
    return df

def csv_to_json(df, config):

    result = []

    for _, row in df.iterrows():
        row_dict = {}
        for col in df.columns:
            row_dict[col] = {"value": row[col]}
        
        result.append(row_dict)

    return result

def get_status(df):
    df["isActive"] = df["isActive"].astype(str).replace(["True", "False"], ["Active", "Inactive"])
    return df


""" Load functions """
# Check and load payload if it is less than 40 mb.
def check_file_size(path):
    file_size = os.path.getsize(path)

    if (file_size / 1048576) > 40:
        print("File too big.")
        return None
    else:
        with open(path, "r") as infile:
            payload = json.load(infile)
        return payload


""" Logging functions """
def setup_logging(log_dir='logs', log_file='pipeline.log'):
    """
    Sets up logging configuration to log messages to a file and console.
    
    Args:
        log_dir (str): Directory where the log file will be stored.
        log_file (str): Name of the log file.
    """
    # Create the logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Set up the log file path
    log_path = os.path.join(log_dir, log_file)
    
    # Define the logging format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,  # Set the lowest-severity log level that the logger will handle
        format=log_format,  # Format of the log messages
        handlers=[
            logging.FileHandler(log_path),  # Log to the file
            logging.StreamHandler()  # Also log to the console
        ]
    )
    
    # Log startup message
    logging.info("Logging initialized. Log file: %s", log_path)