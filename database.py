import pymysql

# Open database connection
db = pymysql.connect("localhost", "root", "", "test")
# print ("happy")
# prepare a cursor object using cursor() method
cursor = db.cursor()
print("Connection Successfully")

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

# disconnect from server
db.close()
