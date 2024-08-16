import datetime
import hashlib
import random
import classesdb
from db import ConnectoMariaDB

SessionTokens = {"4339ulrik@gmail.com": "10a3f9ea81f15a045197d0afa900930081489c363acb934d7aa3125c1f32540dea17e0d47612a70fcf3707c35573372033214ffdb9314e5c636a2d0f45920a9d"}

# Creates a user account if not exist in DB
async def CreateAccount(data: classesdb.CreateUserBase):
    try:
        # Hash password
        pw = hashlib.sha512(str(data.Password).encode('utf-8')).hexdigest()

        # Create the sql data allready converted to dict from fastapi
        MYDB = await ConnectoMariaDB()
        dbcursor = MYDB.cursor()
        sqluseraccounts = "INSERT INTO UserAccounts VALUES (%s, %s, %s, 8)"
        sqluseraccountsVAl: list = [data.Email, data.Username, pw]

        # Create the sql data allready converted to dict from fastapi
        sqluserdata = "INSERT INTO UserData VALUES (%s, 0, 5000, 0, 'Unemployed', 'none')"
        sqluserdataVAl: list = [data.Email]

        # Create the user account and data into the Database (DomeneShop SQL MariaDB 10.4)
        dbcursor.execute(sqluseraccounts, sqluseraccountsVAl)
        dbcursor.execute(sqluserdata, sqluserdataVAl)
        MYDB.commit()

        # If rowcount is greater than 0 then DB has pushed the requested data into DB
        # Inthatcase return a positive message or a negative one to enduser
        if dbcursor.rowcount > 0:
            dbcursor.close()
            MYDB.close()
            return {
                "Message": 'User Created',
                "Error": "No Error specified",
                "Status": 1,
            }
        else:
            dbcursor.close()
            MYDB.close()
            return {
                "Message": 'User Exists',
                "Error": "No Error specified",
                "Status": 0,
            }

    except Exception as e:
        return {
            "Message": 'User Exists or a error occoured',
            "Error": str(e),
            "Status": 0,
        }



# Checks if email and password is correct and then give out a session cookie as UUID
async def LoginAccount(data: classesdb.LoginAccountBase):
    try:
        # Hash password
        pw = hashlib.sha512(str(data.Password).encode('utf-8')).hexdigest()

        # Create the sql data allready converted to dict from fastapi
        MYDB = await ConnectoMariaDB()
        dbcursor = MYDB.cursor()
        sqluseraccounts = "SELECT Password FROM UserAccounts WHERE Email=%s"
        sqluseraccountsVAl: list = [data.Email]

        # Get user account from DB and return the list
        dbcursor.execute(sqluseraccounts, sqluseraccountsVAl)
        dbresult = dbcursor.fetchall()
        
        # Does password match
        if pw == dbresult[0][0]:
            dbcursor.close()
            MYDB.close()

            # Create Token for login every json from createjtoken is sendt in return here if login is OK
            return await CreateJToken(data)
        else:
            dbcursor.close()
            MYDB.close()
            return {
                "Message": 'Bad username or password',
                "Error": "No Error specifiedr",
                "Status": 0,
                "UUID": "0"
            }

    except Exception as e:
        return {
            "Message": 'Bad username or password',
            "Error": str(e),
            "Status": 0,
            "UUID": "0"
        }

# Create a Session token using email and hash and is valid until loggedout or relogginn
async def CreateJToken(data: classesdb.CreateJTokenBase):
    try:
        global SessionTokens
        SessionTokensvalue = hashlib.sha512(str(random.randint(25,2500)).encode('utf-8')).hexdigest()
        SessionTokens[str(data.Email)] = SessionTokensvalue
        
        return {
            "Message": 'Token Created',
            "Error": "No Error specified",
            "Status": 1,
            "UUID": SessionTokensvalue
        }

    except Exception as e:
        return {
            "Message": 'Try agen later',
            "Error": str(e),
            "Status": 0
        }


# Verify is email and token exist in sessiontokens and if it does return status 1
async def VerifyJToken(data: str):
    try:
        global SessionTokens

        # Split data by -
        data2 = data.split('-')

        if SessionTokens[data2[0]] == data2[1]:
            return {
                "Message": 'Session Verified',
                "Error": "No error specified",
                "Email": data2[0],
                "Status": 1,
            }
        else:
            return {
                "Message": 'Session invalid',
                "Error": str(e),
                "Status": 0,
            }
    except Exception as e:
        return {
            "Message": 'Session invalid',
            "Error": str(e),
            "Status": 0,
        }