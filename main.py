from typing import Union
from fastapi import FastAPI, Request
import uvicorn
import account
import flights
import classesdb

app = FastAPI()


@app.get("/")
async def home():
    return {"Hello": "World"}


# USER ACCOUNTS #
@app.post("/apiv1/createuser")
async def createuser(data: classesdb.CreateUserBase):
    return await account.CreateAccount(data)

@app.post("/apiv1/login")
async def login(data: classesdb.LoginAccountBase):
    return await account.LoginAccount(data)

@app.post("/apiv1/VerifyJToken")
async def verifyJtoken(data: Request):
    return await account.VerifyJToken(data.headers.get('TokenMSFS'))

# FLIGHTS / JOBS #
@app.get("/apiv1/GetAllJobs")
async def getalljobs(req: Request):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await flights.GetAllJobs()
    else:
        return x
    
@app.get("/apiv1/GetRandomJobOffers")
async def GetRandomJobOffers(req: Request):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await flights.GetRandomJobOffers(x['Email'])
    else:
        return x

# START WEBSERVER
if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    print("\n Server starting...")
    server.run()


# Check if session is valid
async def ValidateSession(data):
    return await account.VerifyJToken(data)
