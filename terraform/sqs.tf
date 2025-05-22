# Allow S3 to send messages to SQS
resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.population_queue.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "AllowS3SendMessage",
        Effect    = "Allow",
        Principal = "*",
        Action    = "SQS:SendMessage",
        Resource  = aws_sqs_queue.population_queue.arn,
        Condition = {
          ArnLike = {
            "aws:SourceArn" = aws_s3_bucket.raw_data_bucket.arn
          }
        }
      }
    ]
  })
}

# Add bucket notification (trigger on population.json upload)
resource "aws_s3_bucket_notification" "s3_to_sqs" {
  bucket = aws_s3_bucket.raw_data_bucket.id

  queue {
    queue_arn     = aws_sqs_queue.population_queue.arn
    events        = ["s3:ObjectCreated:Put"]
    filter_prefix = "population/"
    filter_suffix = "population.json"
  }

  #  Ensure the SQS policy is created first
  depends_on = [
    aws_sqs_queue_policy.allow_s3
  ]
}
