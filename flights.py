import classesdb
import random
import datetime
from db import MYDB


# Get all the avilable jobs in database and return it back to end user as json list
async def GetAllJobs():
    try:
        dbcursor = MYDB.cursor()
        dbcursor.execute("SELECT * FROM Jobs")
        returndata = []

        # Loop thru data given from DB and return it into list
        for (Company, Available, Used) in dbcursor:
            returndata.append(f"{Company}-{Available}-{Used}")

        # If succesfull close the db and return the data
        dbcursor.close()
        return {
            "Message": 'Data gathered',
            "Error": "No Error specified",
            "Status": 1,
            "Data": returndata
        }
    except Exception as e:
        return {
            "Message": 'No data gathered',
            "Error": str(e),
            "Status": 0,
            "Data": ""
        }


