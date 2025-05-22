resource "aws_s3_bucket" "raw" {
  bucket = var.s3_bucket_name
  force_destroy = true
}
