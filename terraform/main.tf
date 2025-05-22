provider "aws" {
  region = "ap-south-1"
}

# S3 Bucket
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket        = "rearc-data-raw"
  force_destroy = true
}

# SQS Queue
resource "aws_sqs_queue" "population_queue" {
  name                      = "population-json-upload-queue"
  visibility_timeout_seconds = 300
}

# IAM Role for Lambda (used by ingestion Lambda only)
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy Attachment for CloudWatch Logging
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function for ingestion
resource "aws_lambda_function" "lambda_ingest" {
  function_name = "lambda-ingest"
  role          = aws_iam_role.lambda_exec.arn
  runtime       = "python3.10"
  handler       = "lambda_function.lambda_handler"

  filename         = "${path.module}/../lambda_ingest.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda_ingest.zip")

  timeout = 60
}
