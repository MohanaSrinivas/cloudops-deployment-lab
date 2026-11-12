#!/usr/bin/env bash
set -euo pipefail
if ! command -v terraform >/dev/null 2>&1; then echo "Terraform not installed; skipping."; exit 0; fi
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate
