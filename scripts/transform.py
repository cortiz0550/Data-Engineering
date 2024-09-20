import pandas as pd
import os
import utils

# We need to change any TRUE values in isActive to "Active" and FALSE to "Inactive"
def get_status(df):
    df["isActive"] = df["isActive"].astype(str).replace(["True", "False"], ["Active", "Inactive"])
    return df

def csv_to_json(df, config):

    result = []

    for _, row in df.iterrows():
        row_dict = {}
        for col in df.columns:
            row_dict[col] = {"value": row[col]}
        
        result.append(row_dict)

    return result


""" Here we want to start with gathering the config files """
base_path = os.getcwd()
qb_config_path = base_path + "\\config\\quickbase_config.json"
input_path = base_path + "\\data\\raw\\"
output_path = base_path + "\\data\\processed\\" # change this if you want to put the data somewhere else.

# Columns to drop. Add more as needed. This could be part of the config file too.
columns_to_drop = ["lastModified"]

# Load config to get column rename values.
config = utils.load_config(qb_config_path)
column_names = config.get("column_ids")

# Get the data from datalake
df = pd.read_csv(input_path + "survey_list.csv")

# Clean up the dataset a bit.
df.drop(columns=columns_to_drop, axis=1, inplace=True)
df["creationDate"] = df["creationDate"].str[:10] # Keep just the day. This can be changed later if desired.
df = get_status(df)


# Rename columns to match Quickbase ids.
df.rename(columns=column_names, inplace=True)

# Create the payload to send to QB.
cleaned_survey_list = {
    "to": config.get("table_id"),
    "data": csv_to_json(df, config)
}

# Send the data back to staging for upload to Quickbase.
utils.store_surveys(cleaned_survey_list, path=output_path, filename="cleaned_survey_list.json")

