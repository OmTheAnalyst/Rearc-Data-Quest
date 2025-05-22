import boto3
import pandas as pd
import requests
import os
import io

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    # Read the TSV file from S3
    response = s3.get_object(Bucket=bucket_name, Key="pr.data.0.Current")
    series_data = response['Body'].read().decode("utf-8")
    series = pd.read_csv(io.StringIO(series_data), delimiter="\t")

    # Read the JSON file from S3
    response = s3.get_object(Bucket=bucket_name, Key="population.json")
    population_json = response['Body'].read().decode("utf-8")
    population = pd.json_normalize(requests.models.json.loads(population_json), record_path="data")

    # Filter population between years 2013–2018
    filtered = population[
        (population["Year"].astype(int) >= 2013) &
        (population["Year"].astype(int) <= 2018)
    ]

    print("Mean population:", filtered["Population"].mean())
    print("Std Dev population:", filtered["Population"].std())

    series.columns = series.columns.str.strip()
    print("Series data head:")
    print(series.head())
