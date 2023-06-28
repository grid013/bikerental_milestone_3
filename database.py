# import sqlite3
import psycopg2
from psycopg2 import Error
import os

try:
	connection = psycopg2.connect(os.environ["DATABASE_URL"])
	#database instance
	# conn = sqlite3.connect('database.db')
	cursor = connection.cursor()
	#tables
	cursor.execute('''CREATE TABLE users 
			(userId SERIAL PRIMARY KEY, 
			password TEXT,
			email TEXT,
			first_name TEXT,
			last_name TEXT,
			age INTEGER,
			address TEXT,
			userType TEXT,
			createDate TEXT
			)''')
	connection.commit()

	cursor.execute('''CREATE TABLE bikes
			(bikeId SERIAL PRIMARY KEY,
			userId INTEGER,
			bikeName TEXT,
			description TEXT,
			engine TEXT,
			mileage TEXT,
			transmission TEXT,
			price REAL,
			image TEXT,
			createDate TEXT,
			updateDate TEXT,
			status INTEGER DEFAULT 1,
			FOREIGN KEY(userId) REFERENCES users(userId)
			)''')
	connection.commit()

	cursor.execute('''CREATE TABLE comment 
			(commentId SERIAL PRIMARY KEY,
			userId INTEGER,
			bikeId INTEGER,
	      ratings INTEGER,
			message TEXT,
			createDate TEXT,
			FOREIGN KEY(userId) REFERENCES users(userId),
			FOREIGN KEY(bikeId) REFERENCES bikes(bikeId)
			)''')
	connection.commit()

	print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
