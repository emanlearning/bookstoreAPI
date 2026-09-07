import datetime
from pydantic import BaseModel

class Book(BaseModel):
    name: str
    price: float= 10.0
    year: datetime.datetime


book1 = {"name" : "anum", "price": 11.0, "year": datetime.datetime.now()}

book_object = Book(**book1)

print(book_object.name)
print(book_object.price)

def print_book(book):
    print(book)


print_book(book_object)