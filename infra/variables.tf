variable "aws_region" {
 default = "us-east-1"
}
variable "bucket_name" {
  default = "auto-bucket-health-data-monitor"
}

resource "random_id" "suffix" {
  byte_length = 4
}