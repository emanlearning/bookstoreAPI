from fastapi import FastAPI, Depends, HTTPException
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token, check_jwt_token
from models.jwt_user import JWTUser
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY, REDIS_URL, TESTING, IS_LOAD_TEST, IS_PRODUCTION, REDIS_URL_PRODUCTION
from utils.db_object import db
import utils.redis_object as re
# from utils.redis_object import REDIS_CONNECTION_URL
import redis.asyncio as aioredis
from utils.redis_object import check_test_redis
import pickle


app = FastAPI(title="Bookstore API Documentation",description="It's an API thats used for Bookstore", version="1.0.0")

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token),Depends(check_test_redis)],)
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token),Depends(check_test_redis)],)

# app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token)])
# app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])


@app.on_event("startup")
async def connect_db():
    if not TESTING:
        await db.connect()
        if IS_PRODUCTION:
            re.redis = aioredis.from_url(REDIS_URL_PRODUCTION)
        else:
            re.redis = aioredis.from_url(REDIS_URL)


    # # 1. Connect the Database (respecting your flags)
    # await db.connect()
    #
    # # 2. Connect Redis using the CORRECT URL (port 6380 if Load Balancer is True)
    # re.redis = aioredis.from_url(REDIS_CONNECTION_URL)
    #
    # print(f"Server started. Connected to Redis at: {REDIS_CONNECTION_URL}")


@app.on_event("shutdown")
async def disconnect_db():
    if not TESTING:
        await db.disconnect()
        await re.redis.aclose()


@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY, tags=["Post"])
async def login_for_token_access(form_data: OAuth2PasswordRequestForm = Depends()):
    redis_key = f"token:{form_data.username},{form_data.password}"
    user = await re.redis.get(redis_key)

    if not user:
        jwt_user_dict = {"username": form_data.username,
                         "password": form_data.password}
        jwt_user = JWTUser(**jwt_user_dict)
        user = await authenticate_user(jwt_user)

        await re.redis.set(redis_key, pickle.dumps(user))

        if user is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect username or password.")

    else:
        user = pickle.loads(user)

    jwt_token = create_jwt_token(user)
    # print(jwt_user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()

    response = await call_next(request)

    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["execution_time"] = str(execution_time)
    return response
