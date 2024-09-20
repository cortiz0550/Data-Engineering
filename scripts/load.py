
from scripts.utils import get_paths, make_api_request, load_config, check_file_size


def load_data():
    """ Here we want to start with gathering the config files """
    paths = get_paths()
    qb_config_path = paths.get("base_path") + paths.get("qb_config_path")
    processed_data_path = paths.get("base_path") + paths.get("processed_data_path")

    config = load_config(qb_config_path)
    config["api_key"] = "QB-User-Token " + config.get("api_key")


    # Get headers and payload for request
    url = config.get("base_url")
    headers = {
        "Content-Type": "application/json",
        "QB-Realm-Hostname": config.get("realm"),
        "Authorization": config.get("api_key")
    }
    payload = check_file_size(processed_data_path + "cleaned_survey_list.json")


    # Test api call
    req = make_api_request(url=url, method="POST", headers=headers, data=payload)

    # If the payload is empty, we should log that and raise a warning.