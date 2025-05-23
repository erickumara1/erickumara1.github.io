variable "region" {
  default = "us-east-1"
}

variable "zone" {
  default = "us-east-1a"
}

# instance type
variable "instance_type" {
  default = "t4g.nano"
}

variable "bid_price" {
  default = "0.1"
}

variable "target_capacity_type" {
  default = "spot"
}

# Update "ami_id"
variable "ami_id" {
}

# Update "key_name" with the key pair name for SSH connection
# Note: it is NOT the path of the pem file
# you can find it in https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#KeyPairs:sort=keyName
variable "key_name" {
}

variable "project_tag" {
}

