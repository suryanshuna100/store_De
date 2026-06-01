import requests
import json
import logging
from datetime import datetime, UTC
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = [
    "Moradabad",
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad"
]

OUTPUT_DIR = "data/raw/weather"


def fetch_weather(city):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        weather_record = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["main"],
            "ingestion_timestamp": datetime.now(UTC).isoformat()
        }

        logging.info(f"Successfully fetched weather for {city}")

        return weather_record

    except Exception as e:
        logging.error(f"Failed to fetch weather for {city}: {e}")
        return None


def save_data(records):
    if not records:
        logging.warning("No records to save")
        return

    today = datetime.now(UTC).strftime("%Y-%m-%d")

    path = os.path.join(
        OUTPUT_DIR,
        f"ingestion_date={today}"
    )

    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "weather.json")

    with open(file_path, "w") as f:
        json.dump(records, f, indent=4)

    logging.info(f"Saved {len(records)} records to {file_path}")


def main():

    all_weather = []

    for city in CITIES:
        record = fetch_weather(city)

        if record:
            all_weather.append(record)

    save_data(all_weather)


if __name__ == "__main__":
    main()