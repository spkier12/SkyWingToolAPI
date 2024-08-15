import mysql.connector


# Domeneshop MariaDB 10.3
async def ConnectoMariaDB():
    try:
        return mysql.connector.connect(
            host="skywingtoolcom01.mysql.domeneshop.no",
            user="skywingtoolcom01",
            password="RGJjPrJnSP5Vy8HCJGeQW3SnS4kPrX52jpqxC4LM2UBN!!dzJnu1WssKjEMqRC",
            database="skywingtoolcom01",

        )
    except Exception as e:
        print(e)
        ConnectoMariaDB()
