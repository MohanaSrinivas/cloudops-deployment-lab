output "instance_public_ip" { value = aws_instance.demo.public_ip }
output "demo_url" { value = "http://${aws_instance.demo.public_ip}" }
