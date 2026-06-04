
import os
import boto3
import logging

from dotenv import load_dotenv
from datetime import datetime, UTC

# ---------------------------------
# Logging Configuration
# ---------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------
# Load Environment Variables
# ---------------------------------
load_dotenv(override=True)

BUCKET_NAME = os.getenv("S3_BUCKET")

# ---------------------------------
# Create S3 Client
# ---------------------------------
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# ---------------------------------
# Current UTC Timestamp
# ---------------------------------
now = datetime.now(UTC)

year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
hour = now.strftime("%H")

# ---------------------------------
# Local Weather File
# ---------------------------------
LOCAL_FILE = os.path.join(
    "data",
    "raw",
    "weather",
    f"year={year}",
    f"month={month}",
    f"day={day}",
    f"hour={hour}",
    "weather.json"
)

# ---------------------------------
# S3 Bronze Path
# ---------------------------------
S3_FILE = (
    f"bronze/weather/"
    f"year={year}/"
    f"month={month}/"
    f"day={day}/"
    f"hour={hour}/"
    f"weather.json"
)

# ---------------------------------
# Upload Function
# ---------------------------------
def upload_to_s3():

    if not os.path.exists(LOCAL_FILE):

        logging.error(
            f"Local file not found: {LOCAL_FILE}"
        )

        return

    try:

        logging.info(
            "Starting upload process..."
        )

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

    except Exception as e:

        logging.error(
            f"Upload failed: {e}"
        )


# ---------------------------------
# Main
# ---------------------------------
if __name__ == "__main__":
    upload_to_s3()