import mysql.connector

# Open database connection
db = mysql.connector.connect(host='localhost', user='root', password='')

# prepare a mycursor object using cursor() method
mycursor = db.cursor()
print("Connection Successfully")

# execute SQL query using execute() method.
mycursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = mycursor.fetchone()
print("Database version : %s " % data)

# disconnect from server
db.close()
