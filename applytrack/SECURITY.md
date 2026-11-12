# Security notes
Never commit `.env` files or real credentials. Use a unique high-entropy JWT secret and strong database password outside local development. This demo has no rate limiting or refresh-token rotation and is not hardened for public production use. Report suspected vulnerabilities privately to the repository owner.
