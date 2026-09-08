import os


JWT_SECRET_KEY = "1f4430b4b4739f6a85a7f7a3fe2b7d031855e26d1880c474cd045606b553b41d"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

TOKEN_DESCRIPTION = "It require username and password, so if given right then return JWT Token to you."
TOKEN_SUMMARY = "It returns JWT Token."

ISBN_DESCRIPTION = "It is unique identifier for books."

DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_HOST_PRODUCTION = "172.29.85.87"
DB_NAME = "bookstore"
DB_URL = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
DB_URL_PRODUCTION = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PRODUCTION}/{DB_NAME}")

UPLOAD_PHOTO_APIKEY = "adb4c5e0c8b3aa107cd1d8889319f43c"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_APIKEY}"


REDIS_URL = "redis://localhost"
REDIS_URL_PRODUCTION = "redis://172.29.85.87"

TESTING = False
IS_LOAD_TEST = False
IS_PRODUCTION  = True if os.environ["PRODUCTION"] == "true" else False

TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_HOST = "172.20.71.237"
TEST_DB_NAME = "test"
TEST_DB_URL = (f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:5433/{TEST_DB_NAME}")

TEST_REDIS_URL = "redis://172.20.71.237:6380"