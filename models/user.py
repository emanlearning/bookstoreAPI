from pydantic import BaseModel
import enum
from fastapi import Query

class Role(str, enum.Enum):
    admin: str = "admin"
    personel: str = "personel"


class User(BaseModel):
    name: str
    password: str
    # mail: str = Query(..., pattern="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    mail: str = Query(..., pattern=r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    # mail: str
    role: Role
