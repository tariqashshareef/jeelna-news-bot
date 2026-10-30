import os
from datetime import datetime

import boto3
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["READER_AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["READER_AWS_SECRET_ACCESS_KEY"],
)

bucket = os.environ["S3_BUCKET"]

st.title("Sudan Weekly News Report")

response = s3.list_objects_v2(Bucket=bucket, Prefix="reports/")
keys = sorted([item["Key"] for item in response.get("Contents", [])], reverse=True)

if keys:
    key = keys[0]
    text = key.replace("reports/", "").replace(".md", "")
    when = datetime.strptime(text, "%Y-%m-%d")
    st.caption("Latest as of " + when.strftime("%B %d, %Y"))
    st.markdown(s3.get_object(Bucket=bucket, Key=keys[0])["Body"].read().decode("utf-8"))
else:
    st.info("No reports yet")

def latest_run():
    response = requests.get(
        "https://api.github.com/repos/tariqashshareef/jeelna-news-bot/actions/workflows/weekly.yml/runs",
        headers={"Authorization": f"Bearer {os.environ['GH_DISPATCH_TOKEN'].strip()}"},
        params={"per_page": 1},
        timeout=30,
    )
    runs = response.json().get("workflow_runs", [])
    return runs[0] if runs else None

run = latest_run()
running = bool(run) and run["status"] != "completed"

if st.button("Fetch Updated News", disabled=running):
    response = requests.post(
        "https://api.github.com/repos/tariqashshareef/jeelna-news-bot/actions/workflows/weekly.yml/dispatches",
        headers={
            "Authorization": f"Bearer {os.environ['GH_DISPATCH_TOKEN'].strip()}",
            "Accept": "application/vnd.github+json",
        },
        json={"ref": "master"},
        timeout=30,
    )
    if response.status_code == 204:
        st.success("Weekly fetch initiated. Please refresh in a few minutes.")
    else:
        st.error(f"Could not start: {response.status_code}")

if running:
    st.info("A run is currrently in progress. Please refresh in a few minutes.")
