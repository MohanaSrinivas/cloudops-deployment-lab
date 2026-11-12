def register_and_login(client, email="student@example.com"):
    response = client.post("/auth/register", json={"email": email, "password": "correct-horse-42"})
    assert response.status_code == 201
    token = client.post("/auth/login", data={"username": email, "password": "correct-horse-42"})
    assert token.status_code == 200
    return {"Authorization": f"Bearer {token.json()['access_token']}"}

def test_health_and_openapi(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert "openapi" in client.get("/openapi.json").json()

def test_registration_duplicate_and_login(client):
    register_and_login(client)
    assert client.post("/auth/register", json={"email": "student@example.com", "password": "correct-horse-42"}).status_code == 409

def test_crud_statistics_and_user_isolation(client):
    headers = register_and_login(client)
    created = client.post("/applications", headers=headers, json={"company":"Example GmbH","role":"Working Student Python","status":"applied","notes":"Applied online"})
    assert created.status_code == 201
    item_id = created.json()["id"]
    assert client.get("/applications", headers=headers).json()[0]["company"] == "Example GmbH"
    assert client.get("/applications/statistics", headers=headers).json()["total"] == 1
    other = register_and_login(client, "other@example.com")
    assert client.get(f"/applications/{item_id}", headers=other).status_code == 404
    assert client.patch(f"/applications/{item_id}", headers=headers, json={"status":"interview"}).json()["status"] == "interview"
    assert client.delete(f"/applications/{item_id}", headers=headers).status_code == 204
