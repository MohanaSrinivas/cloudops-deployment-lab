# API quick example
After registering and logging in, copy `access_token` and send:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/applications
```
Create:
```bash
curl -X POST http://localhost:8000/applications -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"company":"Example GmbH","role":"Python Working Student","status":"saved"}'
```
