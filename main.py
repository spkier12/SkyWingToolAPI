from typing import Union
from fastapi import FastAPI
import uvicorn
import account
import classesdb

app = FastAPI()


@app.get("/")
async def home():
    return {"Hello": "World"}


@app.post("/apiv1/createuser")
async def createuser(data: classesdb.CreateUserBase):
    return await account.CreateAccount(data)

@app.post("/apiv1/login")
async def login(data: classesdb.LoginAccountBase):
    return await account.LoginAccount(data)

@app.post("/apiv1/verifyuuid")
async def createuser():
    return {"item_id": "1", "q": "2"}


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    print("\n Server starting...")
    server.run()