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

today = datetime.now().strftime("%Y-%m-%d")

LOCAL_FILE = (
    f"data/raw/weather/ingestion_date={today}/weather.json"
)

S3_FILE = (
    f"raw/weather/ingestion_date={today}/weather.json"
)
#AWS automatically creates the folder structure. 
# The S3 key is just a string that can contain slashes to mimic folders, 
# but they are not actual directories. When you upload a file with a key 
# that includes slashes, S3 will display it as if it's in a folder structure, 
# but it's all stored as a single object in the bucket.
try:
    logging.info(f"Starting upload process...")
    logging.info(f"Source file: {LOCAL_FILE}")
    logging.info(f"Destination: s3://{BUCKET_NAME}/{S3_FILE}")

    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        S3_FILE
    )

    logging.info("Upload completed successfully")

except FileNotFoundError:
    logging.error(f"Local file not found: {LOCAL_FILE}")

except Exception as e:
    logging.error(f"Upload failed: {e}")