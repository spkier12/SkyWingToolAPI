from typing import Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_simple_rate_limiter import rate_limiter
from routes import account, jobs
from misc import payload
import uvicorn


app = FastAPI()
app2 = "test123"

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


class CustomException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    content = {
        "success": False, 
        "error": {
            "message": {
                "Message": exc.message,
                "Error": "No Error specified",
                "Status": 0,
            }
        }
    }
    
    return  {
                "status_code": exc.status_code,
                "content": content,
            }

@app.get("/")
@rate_limiter(limit=3, seconds=60)
async def home():
    return {"Fuck": "You"}


# USER ACCOUNTS #
@app.post("/apiv1/createuser")
@rate_limiter(limit=2, seconds=60*60)
async def CreateUser(data: payload.CreateUserBase):
    return await account.CreateAccount(data)

@app.post("/apiv1/login")
@rate_limiter(limit=3, seconds=60)
async def Login(data: payload.LoginAccountBase):
    return await account.LoginAccount(data)

@app.post("/apiv1/VerifyJToken")
@rate_limiter(limit=10, seconds=60)
async def VerifyJToken(data: Request):
    return await account.VerifyJToken(data.headers.get('TokenMSFS'))

# JOBS #
@app.get("/apiv1/GetAllJobs")
@rate_limiter(limit=2, seconds=30)
async def GetAllJobs(req: Request):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.GetAllJobs()
    else:
        return x

@app.get("/apiv1/GetRandomJobOffers")
@rate_limiter(limit=2, seconds=30)
async def GetRandomJobOffers(req: Request):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.GetRandomJobOffers(x['Email'])
    else:
        return x

@app.post("/apiv1/AcceptJobOffers")
@rate_limiter(limit=2, seconds=60)
async def AcceptJobOffers(req: Request, data: payload.AcceptJobOffers):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.AcceptJobOffers(x['Email'], data.Job)
    else:
        return x

@app.post("/apiv1/ApplyForJobs")
@rate_limiter(limit=2, seconds=30)
async def ApplyForJobs(req: Request, data: payload.AcceptJobOffers):
    x = await ValidateSession(req.headers.get('TokenMSFS'))
    if x['Status'] == 1:
        return await jobs.ApplyForJobs(x['Email'], data.Job)
    else:
        return x


# START WEBSERVER
if __name__ == "__main__":
    config = uvicorn.Config("main:app",host="0.0.0.0", port=5000, log_level="info")
    server = uvicorn.Server(config)
    print("\n Server starting...")
    server.run()


# Check if session is valid
async def ValidateSession(data):
    return await account.VerifyJToken(data)
