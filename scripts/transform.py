from scripts.utils import get_paths, load_config, get_status, store_surveys, csv_to_json, get_file, remove_existing_surveys

# We need to change any TRUE values in isActive to "Active" and FALSE to "Inactive"

def transform_data():
    """ Here we want to start with gathering the config files """
    paths = get_paths()
    qb_config_path = paths.get("base_path") + paths.get("qb_config_path")
    raw_data_path = paths.get("base_path") + paths.get("raw_data_path")
    processed_data_path = paths.get("base_path") + paths.get("processed_data_path")

    # Load config to get column rename values.
    config = load_config(qb_config_path)
    column_names = config.get("column_ids")
    
    # Columns to drop. Add more as needed. 
    columns_to_drop = config.get("columns_to_drop")

    # Get the data from datalake
    df = remove_existing_surveys(raw_data_path)

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
    store_surveys(cleaned_survey_list, path=processed_data_path, filename="cleaned_survey_list.json")