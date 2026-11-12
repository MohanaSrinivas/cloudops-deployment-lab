data "aws_vpc" "default" { default = true }
data "aws_subnets" "default" { filter { name = "vpc-id"; values = [data.aws_vpc.default.id] } }
data "aws_ami" "al2023" {
  most_recent = true
  owners = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}
resource "aws_security_group" "app" {
  name_prefix = "${var.project_name}-"
  description = "Demo HTTP access; restrict CIDRs before production use."
  vpc_id = data.aws_vpc.default.id
  ingress { from_port = 80; to_port = 80; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  egress { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}
resource "aws_instance" "demo" {
  ami = data.aws_ami.al2023.id
  instance_type = var.instance_type
  subnet_id = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.app.id]
  user_data = <<-USERDATA
    #!/bin/bash
    dnf update -y
    dnf install -y docker
    systemctl enable --now docker
    docker run -d --restart always -p 80:8000 --name demo public.ecr.aws/docker/library/python:3.12-slim python -m http.server 8000
  USERDATA
  tags = {
    Name = var.project_name
  }
}
