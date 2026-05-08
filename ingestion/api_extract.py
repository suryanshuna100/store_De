import requests
import json
import logging
from datetime import datetime
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

API_URL = "https://fakestoreapi.com/products"
OUTPUT_DIR = "data/raw/products"

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        logging.info("API call successful")
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

def save_data(data):
    if not data:
        logging.warning("No data to save")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_DIR, f"date={today}")

    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "products.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"Data saved to {file_path}")

def main():
    data = fetch_data()
    save_data(data)

if __name__ == "__main__":
    main()
