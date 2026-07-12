from app.core.security import (
    create_access_token,
    verify_access_token,
)

payload = {
    "sub": "1",
    "role": "admin",
}

token = create_access_token(payload)

print("Token:")
print(token)

decoded = verify_access_token(token)

print("\nDecoded Payload:")
print(decoded)