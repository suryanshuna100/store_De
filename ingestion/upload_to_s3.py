import os
import boto3
import logging
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv(override=True)

BUCKET_NAME = os.getenv("S3_BUCKET")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# Current timestamp
now = datetime.now()

year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
hour = now.strftime("%H")

file_name = now.strftime(
    "%Y%m%d_%H0000_weather.json"
)

# Local file path
LOCAL_FILE = os.path.join(
    "data",
    "raw",
    "weather",
    f"year={year}",
    f"month={month}",
    f"day={day}",
    f"hour={hour}",
    file_name
)

# S3 Bronze path
S3_FILE = (
    f"bronze/weather/"
    f"year={year}/"
    f"month={month}/"
    f"day={day}/"
    f"hour={hour}/"
    f"{file_name}"
)

try:

    logging.info("Starting upload process...")

    logging.info(
        f"Source file: {LOCAL_FILE}"
    )

    logging.info(
        f"Destination: s3://{BUCKET_NAME}/{S3_FILE}"
    )

    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        S3_FILE
    )

    logging.info(
        "Upload completed successfully"
    )

except FileNotFoundError:

    logging.error(
        f"Local file not found: {LOCAL_FILE}"
    )

except Exception as e:

    logging.error(
        f"Upload failed: {e}"
    )