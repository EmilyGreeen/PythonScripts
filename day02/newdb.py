#!/usr/bin/python3

import csv
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = mydb.cursor()


#mycursor.execute("CREATE DATABASE emily")
mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)
print()


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "emily"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)
    
sql = "INSERT INTO customers (name, address) VALUES (%s,%s)"
val = ("John","Highway 21")
mycursor.execute(sql,val)

mydb.commit()

print(mycursor.rowcount, " record(s) inserted.")



sql = "INSERT INTO customers (name, address) VALUES (%s,%s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633'),
]
mycursor.executemany(sql,val)

mydb.commit()

print(mycursor.rowcount, " record(s) inserted.")

mycursor.execute("SELECT * FROM customers")
for x in mycursor:
    print(x)
    
mycursor.execute("SELECT * FROM customers")
with open("out.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in mycursor.description])
    csv_writer.writerows(mycursor)