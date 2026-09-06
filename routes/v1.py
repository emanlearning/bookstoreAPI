from fastapi import Body, File, APIRouter
from utils.helper_functions import upload_image_to_server
from models.user import User
from models.book import Book
from models.author import Author
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response
from utils.db_functions import (db_insert_personel, db_check_personel, db_get_book_with_isbn,
                                db_get_author, db_get_author_from_id, db_patch_author_name)
app_v1 = APIRouter()
import utils.redis_object as re
import pickle


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["Post"])
async def post_user(user: User):
    await db_insert_personel(user)
    return {"result": "personel is created"}

# querry parameters
@app_v1.post("/login", tags=["Get"])
async def get_user_validaton(username:str=Body(...), password: str=Body(...)):
    redis_key = f"{username}:{password}"
    result = await re.redis.get(redis_key)

    # redis has data
    if result:
        if result == b"true":
            return {"is_valid (redis)": True}
        else:
            return {"is_valid (redis)": False}
    # redis does not have data
    else:
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result), ex=10)

        return {"is_valid (db)": result}


# pet parameters
@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"], tags=["Get"])
async def get_book_with_isbn(isbn: str):
    result = await re.redis.get(isbn)

    if result:
        result_book = pickle.loads(result)
        return result_book
    else:
        book = await db_get_book_with_isbn(isbn)
        author = await db_get_author(book["author"])
        author_obj = Author(**author)
        book["author"] = author_obj
        result_book = Book(**book)

        await re.redis.set(isbn, pickle.dumps(result_book))
        return result_book


@app_v1.get("/author/{id}/book", tags=["Get"])
async def get_author_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)

        return {"books": books}
    else:
        return {"result": "no author with corresponding id"}

# patch mean update
@app_v1.patch("/author/{id}/name")
async def patch_author_name(id : int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "name is updated"}

@app_v1.post("/user/author", tags=["Post"])
async def post_user_and_author(user: User, author: Author):
    return {"user": user, "author": author}


@app_v1.post("/user/photo", tags=["Post"])
async def upload_user_photo(response:Response, profile_photo: bytes = File(...)):
    await upload_image_to_server(profile_photo)
    return {"file_size": len(profile_photo)}

# ssh -L 5432:localhost:5432 -N -f ubuntu@<NEW_IP_ADDRESS>
# sudo docker start bookstore-db