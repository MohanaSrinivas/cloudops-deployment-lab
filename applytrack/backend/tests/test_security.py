from app.security import create_access_token, decode_subject, hash_password, verify_password

def test_password_hash_and_jwt_round_trip():
    hashed = hash_password("a-long-test-password")
    assert hashed != "a-long-test-password"
    assert verify_password("a-long-test-password", hashed)
    assert not verify_password("wrong-password", hashed)
    assert decode_subject(create_access_token("123")) == "123"
