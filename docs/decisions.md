# Architecture decisions
- Compose is the default so reviewers can run the complete demo without cloud credentials.
- Terraform is opt-in and isolated in its own directory.
- The app snapshot is vendored to make this repository reproducible even if the source repo changes.
- Metrics are not fabricated: only Prometheus's own metrics are available until the API is instrumented.
