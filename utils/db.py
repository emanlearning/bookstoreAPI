# import asyncio
from utils.db_object import db
from utils.const import TESTING


async def execute(query, is_many, values):
    if TESTING:
        await db.connect()

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    if TESTING:
        await db.disconnect()


async def fetch(query, is_one, values):
    if TESTING:
        await db.connect()

    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        if result is None:
            out = None
        else:
            out = []
            for row in result:
                out.append(row)
                
    if TESTING:
        await db.disconnect()

    return out





# query = ("insert into books(isbn, name, author, year)"
#          "values (:isbn, :name, :author, :year)")
# values = {"isbn": 1, "name": "book1", "author": "author1", "year": 2020}

# asyncio.run(execute(query, True, values))
