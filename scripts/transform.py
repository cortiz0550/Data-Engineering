import pandas as pd
import os
import utils

# We need to change any TRUE values in isActive to "Active" and FALSE to "Inactive"
def get_status(df):
    df["isActive"] = df["isActive"].astype(str).replace(["True", "False"], ["Active", "Inactive"])
    return df


""" Here we want to start with gathering the config files """
base_path = os.getcwd()
config_path = base_path + "\\config\\quickbase_config.json"
input_path = base_path + "\\data\\raw\\"
output_path = base_path + "\\data\\processed\\" # change this if you want to put the data somewhere else.

# Columns to drop. Add more as needed. This could be part of the config file too.
columns_to_drop = ["lastModified"]

# Load config to get column rename values.
config = utils.load_config(config_path)
column_names = config.get("column_names")

# Get the data from datalake
df = pd.read_csv(input_path + "survey_list.csv")

# Clean up the dataset a bit.
df.drop(columns=columns_to_drop, axis=1, inplace=True)
df = get_status(df)

# Rename columns to match Quickbase.
df.rename(columns=column_names, inplace=True)

# Send the data back to staging for upload to Quickbase.
utils.store_surveys(df, path=output_path, filename="cleaned_survey_list.csv")

