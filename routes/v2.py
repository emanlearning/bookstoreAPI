from fastapi import Header, APIRouter
from models.user import User
from starlette.status import HTTP_201_CREATED

app_v2 = APIRouter()


@app_v2.post("/user", status_code=HTTP_201_CREATED, tags=["Post"])
async def post_user(user: User, x_custom: str = Header(...)):
    return {"heyyy im:": "request no2"}
