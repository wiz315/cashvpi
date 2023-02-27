import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

# Token Response
def token_response(token: str):
    return {
        "access_token": token
    }
# Sign JWT
def signJWT(id: str) -> Dict[str, str]:
    payload = {
        "user_id": id,
        "expires": time.time() +600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm= JWT_ALGORITHM)
    return token_response(token)
# decode JWT
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms= [JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}