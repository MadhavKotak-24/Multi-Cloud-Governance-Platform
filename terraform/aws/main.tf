provider "aws" {
  region = "us-east-1"
}

# Unique bucket per deployment
resource "aws_s3_bucket" "app_bucket" {
  bucket = "cloudgov-${var.application}-${var.environment}-${random_id.rand.hex}"

  tags = {
    Application = var.application
    Environment = var.environment
    ManagedBy   = "CloudGovPlatform"
  }
}

# Random suffix to avoid name clashes
resource "random_id" "rand" {
  byte_length = 4
}
