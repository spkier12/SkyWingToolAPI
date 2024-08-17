import classesdb
import random
import datetime
from db import ConnectoMariaDB


GetRandomJobOffersStore = {}

# Get all the avilable jobs in database and return it back to end user as json list
async def GetAllJobs():
    try:

        # Create a new connection to DB
        MYDB = await ConnectoMariaDB()
        dbcursor = MYDB.cursor()

        # Get all jobs available
        dbcursor.execute("SELECT * FROM Jobs")
        returndata = []

        # Loop thru data given from DB and return it into list
        for (Company, Available, Used) in dbcursor:
            returndata.append(f"{Company}-{Available}-{Used}")

        # If succesfull close the db and return the data
        dbcursor.close()
        MYDB.close()
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

# Executing this command gives you 5 random jobs you can join and can only be executed once per user
async def GetRandomJobOffers(Email: str):
    try:

        # Check if user has not allready been given a job offer
        if Email in GetRandomJobOffersStore:
            return {
                "Message": 'You have allready been given job offers',
                "Error": "",
                "Status": 0,
                "Data": ""
            }

        # Create a new connection to DB
        MYDB = await ConnectoMariaDB()
        dbcursor = MYDB.cursor()

        # Check if user does not have a job
        dbcursor.execute("SELECT Job FROM UserData WHERE Email=%s", [Email])
        dbresult = dbcursor.fetchall()
        if dbresult[0][0] != "none":
            dbcursor.close()
            MYDB.close()
            return {
                "Message": 'You allready have a job',
                "Error": "No error specified",
                "Status": 0,
                "Data": ""
            }

        # Get companies in database
        dbcursor.execute("SELECT Company FROM Jobs")

        # Sort everything into list
        returndata = []
        for Company in dbcursor:
            returndata.append(str(Company))

        # Select the random 5 jobs and store them in list
        lastfivejobs = []
        for x in range(5):
             lastfivejobs.append(str(random.choice(returndata)))

        # Close the connection and return the data
        dbcursor.close()
        MYDB.close()
        GetRandomJobOffersStore[Email] = lastfivejobs
        return {
            "Message": '5 Random Job offers has been granted',
            "Error": "No error specified",
            "Status": 1,
            "Data": lastfivejobs
        }
        
    except Exception as e:
        return {
            "Message": 'You allready have asked for 5 random job offers',
            "Error": str(e),
            "Status": 0,
            "Data": ""
        }

# Accept any job you have been offered '
async def AcceptJobOffers(Email: str, Job: str):
    try:

        # Check if user has been given random job offers
        if Email in GetRandomJobOffersStore:
            
            # Get the Jobs available in list and loop thru them until you get the job you wanted
            # And return the happy message back to enduser and update DB
            for x in GetRandomJobOffersStore[Email]:
                print(f"\n Offered: {x} want: {Job}")
                if Job.lower() in str(x).lower():
                    print(f"\n You joined company: {x}")
                    return {
                        "Message": f'You joined company: {x}',
                        "Error": "No error Specified",
                        "Status": 1,
                    }

            # You can only join jobs you have been offered
            return {
                "Message": 'You cannot join a job that has not been offered to you',
                "Error": "No error Specified",
                "Status": 0,
            }
                
        else:
            pass

    except Exception as e:
        return {
            "Message": 'Cannot find any jobs available at the moment...',
            "Error": str(e),
            "Status": 0,
        }