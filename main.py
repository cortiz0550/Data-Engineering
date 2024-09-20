from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data

def main():
    # Step 1: extract the data and store it.
    extract_data()

    # Step 2: Transform the data to match its destination and store it.
    transform_data()

    # Step 3: Load the data into Quickbase.
    load_data()


if __name__ == "__main__":
    main()