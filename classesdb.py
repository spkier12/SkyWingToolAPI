from pydantic import BaseModel

class CreateUserBase(BaseModel):
    Email: str
    Username: str
    Password: str

class LoginAccountBase(BaseModel):
    Email: str
    Password: str