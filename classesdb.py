from pydantic import BaseModel

class CreateUserBase(BaseModel):
    Email: str
    Username: str
    Password: str

class LoginAccountBase(BaseModel):
    Email: str
    Password: str

class CreateJTokenBase(BaseModel):
    Email: str

class VerifyJTokenBase(BaseModel):
    Email: str
    Token: str