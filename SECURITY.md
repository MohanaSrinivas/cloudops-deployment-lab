# Security
Do not commit `.env`, Terraform state, cloud credentials or personal data. The Terraform sample opens port 80 to the internet and is not production safe. Restrict ingress, enable TLS, use IAM least privilege and review all costs before applying. Rotate any credential that is accidentally committed.
