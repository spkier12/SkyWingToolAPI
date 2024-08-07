import mysql.connector

MYDB = mysql.connector.connect(
    host="skywingtoolcom01.mysql.domeneshop.no",
    user="skywingtoolcom01",
    password="RGJjPrJnSP5Vy8HCJGeQW3SnS4kPrX52jpqxC4LM2UBN!!dzJnu1WssKjEMqRC",
    database="skywingtoolcom01",
    # pool_size=3,
    # pool_name="toolcom01"
)

print("\n Connected to DB")