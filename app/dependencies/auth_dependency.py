import os
import time
import jwt
from dotenv import load_dotenv
from jwt.exceptions import ExpiredSignatureError
from fastapi import Header, HTTPException, Depends

from app.utils.responses import response

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
print("Os getenv", JWT_SECRET)


def auth_dependency(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication Token is missing!")

    token = None
    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    else:
        raise HTTPException(status_code=401, detail="Invalid token format!")
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if decoded_token["exp"] < time.time():
            raise HTTPException(status_code=401, detail="Token has expired")

        return decoded_token

    except ExpiredSignatureError:
        return response(401, "Token has expired")

    except Exception as e:
        print("Exception at auth dependency: ", e)
        raise HTTPException(
            status_code=500, detail="Something went wrong", headers={"error": str(e)}
        )
