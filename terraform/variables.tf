variable "aws_region" { type = string; default = "eu-central-1" }
variable "project_name" { type = string; default = "cloudops-lab" }
variable "instance_type" { type = string; default = "t3.micro" }
variable "ssh_public_key" { type = string; default = ""; description = "Optional SSH public key; leave empty to disable SSH ingress." }
