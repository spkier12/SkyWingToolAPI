from typing import Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import uvicorn
import account
import jobs
import classesdb

app = FastAPI()

# Initialize FastAPILimiter
limiter = FastAPILimiter(app)

origins = [
    "http://msfs.skywingtool.com",
    "https://msfs.skywingtool.com",
    "http://api.skywingtool.com",
    "https://api.skywingtool.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@limiter.limit("5/minute")
@app.get("/")
async def home():
    return {"Hello": "World"}


# USER ACCOUNTS #
@limiter.limit("5/minute")
@app.post("/apiv1/createuser")
async def CreateUser(data: classesdb.CreateUserBase):
    return await account.CreateAccount(data)

@limiter.limit("5/minute")
@app.post("/apiv1/login")
async def Login(data: classesdb.LoginAccountBase):
    return await account.LoginAccount(data)

@limiter.limit("5/minute")
@app.post("/apiv1/VerifyJToken")
async def VerifyJToken(data: Request):
    return await account.VerifyJToken(data.headers.get('TokenMSFS'))

# FLIGHTS / JOBS #
@limiter.limit("5/minute")
@app.get("/apiv1/GetAllJobs")
async def GetAllJobs(req: Request):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.GetAllJobs()
    else:
        return x

@limiter.limit("5/minute")
@app.get("/apiv1/GetRandomJobOffers")
async def GetRandomJobOffers(req: Request):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.GetRandomJobOffers(x['Email'])
    else:
        return x

@limiter.limit("5/minute")
@app.post("/apiv1/AcceptJobOffers")
async def AcceptJobOffers(req: Request, data: classesdb.AcceptJobOffers):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.AcceptJobOffers(x['Email'], data.Job)
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
