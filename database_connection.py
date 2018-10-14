import mysql.connector

host = 'localhost'
user = 'root'
password = ''

db_name = 'fo'
table_name = 'fo_data'


# db = mysql.connector.connect(host=host, user=user, password=password)
# mycursor = db.cursor()
# mycursor.execute("SELECT VERSION()")
# data = mycursor.fetchone()
# db.close()


def _check_database():
    conn = mysql.connector.connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'" % db_name
    cursor.execute(query)
    result = cursor.fetchall()
    # print(result)
    if len(result) == 0:
        query = "CREATE DATABASE IF NOT EXISTS %s" % db_name
        cursor.execute(query)
        print("Database created: %s" % db_name)
    else:
        print("Database already present")

    cursor.close()
    conn.close()


def _check_table(truncate: bool):
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    # query = "SELECT table_name FROM information_schema.tables WHERE table_name = '%s'" % table_name
    query = "SELECT table_name FROM information_schema.tables WHERE table_name = '%s'" % table_name
    cursor.execute(query)
    result = cursor.fetchall()
    # print(result)
    if len(result) == 0:
        print("Table not found")
        query = "CREATE TABLE %s (id int NOT NULL AUTO_INCREMENT,instrument varchar(8) ,symbol varchar(30) ," \
                "expiry date,strike int, option_typ varchar(5), open float, high float, low float, close double, " \
                "settle_pr float, contracts int, val float, open_int int, chg_in_oi int, timestamp date, PRIMARY KEY " \
                "(id))" % table_name
        cursor.execute(query)
        print("Table created: %s" % table_name)
    else:
        print("Table already present")
        if truncate:
            truncate = 'TRUNCATE TABLE %s' % table_name
            cursor.execute(truncate)
            print('Table Truncated')
    cursor.close()
    db_conn.close()


def insert_data(queries):
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    for query in queries:
        # print(query)
        cursor.execute(query)
    # result = cursor.fetchall()
    db_conn.commit()
    cursor.close()
    db_conn.close()


def bulk_entries(truncate: bool):
    _check_database()
    _check_table(truncate)

#
# instrument = 'FUTIDX'
#     symbol = 'BANKNIFTY'
#     expiry = '2018-10-25'
#     strike = 00
#     option_typ = 'CE'
#     open_price = 24444.7
#     high = 24816.8
#     low = 24285
#     close = 24712.65
#     settle_pr = 24712.65
#     contracts = 134919
#     val = 132545.25
#     open_int = 1443200
#     chg_in_oi = -62440
#     timestamp = '2018-10-08'
#     header = "INSERT INTO `fo_data`(`instrument`, `symbol`, `expiry`, `strike`, `option_typ`, `open`, `high`, `low`, " \
#              "`close`, `settle_pr`, `contracts`, `val`, `open_int`, `chg_in_oi`, `timestamp`) VALUES "
#     delimiter = ','
#     trailer = "('%s','%s', '%s', %d,'%s', %f, %f, %f, %f, %f, %d, %f, %d, %d, '%s')" % (
#         instrument, symbol, expiry, strike, option_typ, open_price, high, low, close, settle_pr, contracts, val,
#         open_int, chg_in_oi, timestamp)
#     query = header + trailer
# bulk_entries()
