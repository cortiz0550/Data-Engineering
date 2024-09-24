import logging
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data

def main():
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Step 1: Extract survey data
        logging.info("Starting data extraction...")
        extract_data()
        
        # Step 2: Transform the data
        logging.info("Transforming data...")
        transform_data()
        
        # Step 3: Load the data into the destination
        logging.info("Loading data...")
        load_data()
        
        logging.info("Data pipeline completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
