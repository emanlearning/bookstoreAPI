from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import (
                         JWT_SECRET_KEY,
                         JWT_ALGORITHM,
                         JWT_EXPIRATION_TIME_MINUTES
)
import jwt
from fastapi import Depends, HTTPException
import time
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from utils.db_functions import db_check_token_user, db_check_jwt_username
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

# create hashed password
def get_hashed_password(password: str):
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Convert bytes to string before returning so it saves correctly in DB
    return hashed_password.decode('utf-8')


# verify hashed password with plain password
def verify_password(plain_password: str, hashed_password: str):
    try:
        # plain_password comes from the login form
        # hashed_password comes from the database
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False


# Authenticate username and password to give JWT token
async def authenticate_user(user:JWTUser):
    # hashed_password = get_hashed_password(user.password)
    # user.password = hashed_password

    potential_users = await db_check_token_user(user)

    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True
    if is_valid:
        user.role = "admin"
        return user

    return None


# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username,
                   "role": user.role,
                   "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return jwt_token


# Check whether the JWT is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                return final_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="error in security.py/check_jwt_token")

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

