"""Stores a file to the S3 bucket."""

import os

import boto3
from dotenv import load_dotenv

load_dotenv()
bucket = os.environ["S3_BUCKET"]

s3 = boto3.client("s3")

def upload(path, key):
    """
    Uploads a local file to the S3 news bucket.

    Args:
        path: Path of the local file to upload.
        key: Object key in the bucket, such as "reports/<current_date>.md".
    """
    
    s3.upload_file(path, bucket, key)