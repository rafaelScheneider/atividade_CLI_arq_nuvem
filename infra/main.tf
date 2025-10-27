provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_object" "folders" {
  for_each = toset(["raw/", "trusted/", "client/"])
  bucket   = aws_s3_bucket.data_bucket.id
  key      = each.value
}

output "bucket_name" {
  value = aws_s3_bucket.data_bucket.bucket
}
