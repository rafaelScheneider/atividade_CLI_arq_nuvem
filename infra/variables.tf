variable "aws_region" {
 default = "us-east-1"
}
variable "bucket_name" {
  default = "lab-sprint5-arqnuvem-rafael-scheneider"
}

resource "random_id" "suffix" {
  byte_length = 4
}