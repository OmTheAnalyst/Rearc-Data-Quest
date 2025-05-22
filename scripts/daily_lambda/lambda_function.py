import os
import requests
import boto3
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup

BASE_URL = "https://download.bls.gov/pub/time.series/pr/"
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_PREFIX = "bls/"

HEADERS = {
    "User-Agent": "om.pandey@example.com (for academic/data engineering project)"
}

s3 = boto3.client("s3")

def get_file_list():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    filenames = [
        os.path.basename(link.get("href"))
        for link in links
        if link.get("href") and not link.get("href").endswith("/")
    ]
    return filenames

def download_file(filename):
    file_url = f"{BASE_URL}{filename}"
    response = requests.get(file_url, headers=HEADERS)
    if response.status_code == 200:
        return response.content
    print(f"Could not download {filename}")
    return None

def upload_to_s3(filename, content):
    key = f"{S3_PREFIX}{filename}"
    try:
        s3.head_object(Bucket=S3_BUCKET, Key=key)
        print(f"{filename} already exists in S3, skipping.")
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"Uploading {filename} to S3...")
            s3.put_object(Bucket=S3_BUCKET, Key=key, Body=content)
        else:
            print(f"Error checking {filename} in S3: {str(e)}")

def lambda_handler(event, context):
    if not S3_BUCKET:
        raise ValueError("S3_BUCKET_NAME environment variable not set")

    files = get_file_list()
    print(f"Found {len(files)} files on BLS server.")
    for file in files:
        content = download_file(file)
        if content:
            upload_to_s3(file, content)

    # Upload population data
    pop_response = requests.get("https://datausa.io/api/data?drilldowns=Nation&measures=Population")
    if pop_response.status_code == 200:
        s3.put_object(Bucket=S3_BUCKET, Key="population/population.json", Body=pop_response.text)
        print("Uploaded population.json to S3.")
    else:
        print("Failed to download population API data")

    return "Lambda Ingest Complete"
