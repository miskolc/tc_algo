import time

import mysql.connector

import options
from constants import Keys
from options import greeks_calculator, test

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


def add_greeks_column():
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    check_query = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'fo' AND TABLE_NAME = 'fo_data2' AND COLUMN_NAME LIKE 'iv'"
    cursor.execute(check_query)
    check = cursor.fetchall()
    if len(check) == 0:
        print('Adding Columns to the table...')
        query = "ALTER TABLE %s ADD (iv float, theta float, gamma float, delta float, vega float)" % "fo_data2"
        cursor.execute(query)
    else:
        print("Column already present")
    db_conn.close()


index_id = 0
instrument_id = 1
symbol_id = 2
expiry_id = 3
strike_id = 4
option_type_id = 5
open_id = 6
high_id = 7
low_id = 8
close_id = 9
settle_id = 10
contracts_id = 11
val_id = 12
open_int_id = 13
chg_in_oi = 14
timestamp_id = 15

interest = 0.0


#
# def update_database_greeks():
#     queries = []
#     db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
#     cursor = db_conn.cursor()
#     db_conn1 = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
#     cursor1 = db_conn1.cursor()
#     # cursor1 = db_conn.cursor()
#     # query = "SELECT distinct symbol FROM `fo_data2` where instrument='FUTIDX' order by timestamp asc"
#     # query = "SELECT * FROM `fo_data2` WHERE instrument='OPTIDX' AND timestamp='2018-08-01' "
#     query = "SELECT * FROM `fo_data2` WHERE instrument LIKE 'OPT%' ORDER BY id ASC LIMIT 1000"
#     cursor.execute(query)
#     for row in cursor:
#         index = row[index_id]
#         symbol = row[symbol_id]
#         strike = (row[strike_id])
#         expiry = row[expiry_id]
#         option_type = row[option_type_id]
#         price = row[close_id]
#         timestamp = row[timestamp_id]
#         # print(index, symbol, strike, expiry, option_type, price)
#         underlying_query = "SELECT close FROM %s WHERE instrument LIKE 'FUT%%' AND symbol = '%s' AND MONTH(expiry) = %s" % (
#             'fo_data2', symbol, expiry.month)
#         # print(underlying_query)
#         cursor1.execute(underlying_query)
#         underlying_price = float(cursor1.fetchall()[0][0])
#         # print(index, symbol, strike, expiry, option_type, price, underlying_price)
#         # greeks = None
#         iv, theta, gamma, delta, vega = 0, 0, 0, 0, 0
#         if option_type == 'CE':
#             iv = greeks_calculator.implied_vol(underlying_price, strike, interest, expiry, call_price=price)
#             # greeks = greeks_calculator.option_price()
#         if option_type == 'PE':
#             iv = greeks_calculator.implied_vol(underlying_price, strike, interest, expiry, put_price=price)
#             # greeks = greeks_calculator.option_price(underlying_price, strike, interest, expiry, iv, timestamp)
#
#         greeks = greeks_calculator.option_price(underlying_price, strike, interest, expiry, iv, timestamp)
#         if greeks is not None:
#             theta = greeks.call_theta if option_type == 'CE' else greeks.put_theta
#             delta = greeks.call_delta if option_type == 'CE' else greeks.put_delta
#             gamma = greeks.gamma
#             vega = greeks.vega
#
#         # db_conn1.close()
#         print(index, symbol, strike, expiry, option_type, price, underlying_price, iv, theta, gamma, delta, vega)
#         update_query = "UPDATE `%s` SET `iv`=%s,`theta`=%s,`gamma`=%s,`delta`=%s,`vega`=%s WHERE id=%d" % (
#             "fo_data2", iv, theta, gamma, delta, vega, index)
#         queries.append(update_query)
#     # print(type(row))
#     # while True:
#     #     print(cursor.fetchone())
#     # cursor.close()
#     # cursor1.execute(queries)
#     print(len(queries))
#     db_conn1.close()
#     db_conn.close()


def update_database_greeks():
    queries = []
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    # db_conn1 = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    # cursor1 = db_conn1.cursor()
    timestamp_query = 'SELECT distinct timestamp from fo_data2 ORDER BY timestamp ASC'
    cursor.execute(timestamp_query)
    x = cursor.fetchall()
    for ts in x:
        data_date = ts[0]
        fut_data = get_fut_data(data_date)
        opt_query = "SELECT * FROM `fo_data2` WHERE instrument LIKE 'OPT%%' AND timestamp='%s' ORDER BY id ASC Limit 300" % data_date
        cursor.execute(opt_query)
        opt_data = cursor.fetchall()
        for row in opt_data:
            instrument = row[instrument_id]
            index = row[index_id]
            symbol = row[symbol_id]
            strike = (row[strike_id])
            expiry = row[expiry_id]
            option_type = row[option_type_id]
            price = row[close_id]
            timestamp = row[timestamp_id]
            # print(index, symbol, strike, expiry, option_type, price)
            # underlying_query = "SELECT close FROM %s WHERE instrument LIKE 'FUT%%' AND symbol = '%s' AND MONTH(expiry) = %s" % (
            #     'fo_data2', symbol, expiry.month)
            # cursor.execute(underlying_query)
            # key = "%s_%s_%s_%s" % ()
            key = "%s_%s_%s_%s" % (instrument[3:], symbol, expiry.month, expiry.year)
            try:
                underlying_price = fut_data[key]
                # if option_type == 'CE':
                #     iv = greeks_calculator.implied_vol(underlying_price, strike, interest, expiry, timestamp=timestamp, call_price=price)
                #     # greeks = greeks_calculator.option_price()
                # if option_type == 'PE':
                #     iv = greeks_calculator.implied_vol(underlying_price, strike, interest, expiry, timestamp=timestamp, put_price=price)
                #     # greeks = greeks_calculator.option_price(underlying_price, strike, interest, expiry, iv, timestamp)

                # Keys.call if option_type == 'CE' else Keys.put
                greeks = test.get_greeks(underlying_price, strike, expiry, option_type, price, timestamp,
                                         volatility=13.65)
                print(greeks)
            except KeyError:
                print("Couldn't find %s" % key)
            # print(underlying_price)
    #         iv, theta, gamma, delta, vega = 0, 0, 0, 0, 0
    #         if option_type == 'CE':
    #             iv = greeks_calculator.implied_vol(underlying_price, strike, interest, expiry, call_price=price)
    #             # greeks = greeks_calculator.option_price()
    #         if option_type == 'PE':
    #             iv = greeks_calculator.implied_vol(underlying_price, strike, interest, expiry, put_price=price)
    #             # greeks = greeks_calculator.option_price(underlying_price, strike, interest, expiry, iv, timestamp)
    #
    #         greeks = greeks_calculator.option_price(underlying_price, strike, interest, expiry, iv, timestamp)
    #         if greeks is not None:
    #             theta = greeks.call_theta if option_type == 'CE' else greeks.put_theta
    #             delta = greeks.call_delta if option_type == 'CE' else greeks.put_delta
    #             gamma = greeks.gamma
    #             vega = greeks.vega
    #
    #         # db_conn1.close()
    #         print(index, symbol, strike, expiry, option_type, price, underlying_price, iv, theta, gamma, delta, vega)
    #         update_query = "UPDATE `%s` SET `iv`=%s,`theta`=%s,`gamma`=%s,`delta`=%s,`vega`=%s WHERE id=%d" % (
    #             "fo_data2", iv, theta, gamma, delta, vega, index)
    #         queries.append(update_query)
    # print(len(queries))
    db_conn.close()


def get_fut_data(timestamp):
    data = {}
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    underlying_query = "SELECT * FROM %s WHERE instrument LIKE 'FUT%%' AND timestamp = '%s'" % ('fo_data2', timestamp)
    cursor.execute(underlying_query)
    fut_data = cursor.fetchall()
    for fut in fut_data:
        instrument = fut[instrument_id]
        symbol = fut[symbol_id]
        expiry = fut[expiry_id]
        close = fut[close_id]
        key = "%s_%s_%s_%s" % (instrument[3:], symbol, expiry.month, expiry.year)
        data.update({key: close})
    db_conn.close()
    # print(data)
    return data


start_time = time.time()
# add_greeks_column()
update_database_greeks()
print("Time Taken: %s" % (time.time() - start_time))
