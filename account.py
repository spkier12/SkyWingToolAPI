import hashlib
import classesdb
from db import MYDB

# Creates a user account if not exist in DB
async def CreateAccount(data: classesdb.CreateUserBase):
    try:
        # Hash password
        pw = hashlib.sha512(str(data.Password).encode('utf-8')).hexdigest()

        # Create the sql data allready converted to dict from fastapi
        dbcursor = MYDB.cursor()
        sqluseraccounts = "INSERT INTO UserAccounts VALUES (%s, %s, %s, 8)"
        sqluseraccountsVAl: list = [data.Email, data.Username, pw]

        # Create the sql data allready converted to dict from fastapi
        sqluserdata = "INSERT INTO UserData VALUES (%s, 0, 5000, 0, 'Unemployed')"
        sqluserdataVAl: list = [data.Email]

        # Create the user account and data into the Database (DomeneShop SQL MariaDB 10.4)
        dbcursor.execute(sqluseraccounts, sqluseraccountsVAl)
        dbcursor.execute(sqluserdata, sqluserdataVAl)
        MYDB.commit()

        # If rowcount is greater than 0 then DB has pushed the requested data into DB
        # Inthatcase return a positive message or a negative one to enduser
        if dbcursor.rowcount > 0:
            dbcursor.close()
            return {
                "Message": 'User Created',
                "Error": "No Error specified"
            }
        else:
            dbcursor.close()
            return {
                "Message": 'User Exists',
                "Error": "No Error specified"
            }

    except Exception as e:
        return {
            "Message": 'Try agen later',
            "Error": str(e)
        }



# Checks if email and password is correct and then give out a session cookie as UUID
async def LoginAccount(data: classesdb.LoginAccountBase):
    try:
        # Hash password
        pw = hashlib.sha512(str(data.Password).encode('utf-8')).hexdigest()

        # Create the sql data allready converted to dict from fastapi
        dbcursor = MYDB.cursor()
        sqluseraccounts = "SELECT Password FROM UserAccounts WHERE Email=%s"
        sqluseraccountsVAl: list = [data.Email]

        # Get user account from DB and return the list
        dbcursor.execute(sqluseraccounts, sqluseraccountsVAl)
        dbresult = dbcursor.fetchall()
        
        # Does password match
        if pw == dbresult[0][0]:
            dbcursor.close()
            return {
                "Message": 'Login succsesfull',
                "Error": "No error",
                "UUID": "02"
            }
        else:
            dbcursor.close()
            return {
                "Message": 'Bad username or password',
                "Error": "No error",
                "UUID": "0"
            }

    except Exception as e:
        return {
            "Message": 'Bad username or password',
            "Error": str(e),
            "UUID": "0"
        }

