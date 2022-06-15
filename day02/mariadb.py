#!/usr/bin/python3

import os
import mysql.connector as database

connection = database.connect(	user="root",
								password="root",
								host="localhost", 
								database="sakila"
								)
cursor = connection.cursor()

def getData():
	try:
		statement = "SELECT title FROM film;"
		cursor.execute(statement)
		for title in cursor:
			print("Title: ",title)
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")
	connection.close()

getData()
