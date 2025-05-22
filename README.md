Rearc Data Quest - Project Summary
==================================

This project is a complete implementation of the Rearc Data Quest, demonstrating data engineering, automation, and cloud infrastructure skills using AWS, Terraform, and Python.

------------------------------------------------------------
Project Structure:
------------------

rearc-data-quest/
│
├── scripts/
│   ├── daily_lambda/               -> Lambda function for ingestion (BLS + Population)
│   └── analytics_lambda/           -> (Optional) Lambda for analytics (triggered by SQS)
│
├── notebooks/
│   └── part3_analysis.ipynb        -> Notebook for all analytics based on Part 1 and 2 data
│
├── terraform/                      -> Infrastructure-as-Code using Terraform
│
├── data/                           -> (Optional) For testing or staging files locally
│
└── README.txt                      -> This file

------------------------------------------------------------
Completed Tasks:
----------------

Part 1: AWS S3 & Sourcing Datasets
- Downloaded all files from https://download.bls.gov/pub/time.series/pr/
- Synced files to S3 under "bls/" folder
- Handled 403 Forbidden using proper User-Agent header
- Deduplicated existing files and removed outdated ones

Part 2: APIs
- Pulled US population data from: https://datausa.io/api/data?drilldowns=Nation&measures=Population
- Saved the data as a JSON file in S3 under "population/population.json"

Part 3: Data Analytics
- Used pandas to:
  1. Calculate mean and standard deviation of US population (2013–2018)
  2. Find the best year (maximum total value) for each series_id
  3. Join population with specific BLS data (series_id = PRS30006032, period = Q01)

Part 4: Infrastructure as Code (IaC)
- Used Terraform to create:
  - S3 bucket (rearc-data-raw)
  - SQS queue for notifications
  - Lambda function for ingestion (lambda-ingest.zip)
  - Proper IAM roles and policies
- Connected S3 → SQS → Lambda

------------------------------------------------------------
Deployment Instructions:
------------------------

1. Package Lambda using Docker:

docker run -it --rm -v ${PWD}/scripts/daily_lambda:/var/task -w /var/task public.ecr.aws/sam/build-python3.10 /bin/bash

Inside the container:

pip install -r requirements.txt -t .
zip -r /var/task/../../lambda_ingest.zip .
exit

2. Deploy Infra using Terraform:

cd terraform
terraform init
terraform apply -auto-approve

------------------------------------------------------------
S3 Output:
----------

- BLS Files: s3://rearc-data-raw/bls/
- Population Data: s3://rearc-data-raw/population/population.json

------------------------------------------------------------
Author:
-------

OmTheAnalyst (https://github.com/OmTheAnalyst)