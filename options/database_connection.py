import time
from datetime import date

import mysql.connector

from options import option_greeks

host = 'localhost'
user = 'root'
password = ''

db_name = 'fo'
table_name = 'fo_data1'


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
    check_query = "SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' AND COLUMN_NAME LIKE 'iv'" % (
        db_name, table_name)
    cursor.execute(check_query)
    check = cursor.fetchall()
    if len(check) == 0:
        print('Adding Columns to the table...')
        query = "ALTER TABLE %s ADD (iv float, theta float, gamma float, delta float, vega float)" % table_name
        cursor.execute(query)
    else:
        print("Column already present")
    db_conn.close()


# index_id = 0
# instrument_id = 1
# symbol_id = 2
# expiry_id = 3
# strike_id = 4
# option_type_id = 5
# open_id = 6
# high_id = 7
# low_id = 8
# close_id = 9
# settle_id = 10
# contracts_id = 11
# val_id = 12
# open_int_id = 13
# chg_in_oi = 14
# timestamp_id = 15

interest = 0.0


# interest = 0.10 # For spot as per NSE


def _get_fut_data(timestamp):
    data = {}
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    underlying_query = "SELECT * FROM %s WHERE instrument LIKE 'FUT%%' AND timestamp = '%s'" % (table_name, timestamp)
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
    return data


def update_database_greeks(ts: date):
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    # if clear_columns:
    #     print("Clearing the columns...")
    #     columns = ["iv", "theta", "gamma", "delta", "vega"]
    #     for col in columns:
    #         query = "UPDATE %s SET %s=''" % (table_name, col)
    #         cursor.execute(query)
    #         cursor.fetchall()
    #         # db_conn.commit()
    #         print("Cleared: %s" % col)
    if ts is not None:
        timestamp_query = "SELECT distinct timestamp from %s where timestamp = '%s-%s-%s' ORDER BY timestamp ASC " % (
            table_name, ts.year, ts.month, ts.day)
    else:
        timestamp_query = 'SELECT distinct timestamp from %s ORDER BY timestamp ASC' % table_name

    cursor.execute(timestamp_query)
    x = cursor.fetchall()
    for ts in x:
        date_time = time.time()
        data_date = ts[0]
        print("Updating options data for: %s" % data_date)
        fut_data = _get_fut_data(data_date)
        opt_query = "SELECT * FROM `%s` WHERE instrument LIKE 'OPT%%' AND timestamp='%s' ORDER BY id ASC " % (
            table_name, data_date)
        cursor.execute(opt_query)
        opt_data = cursor.fetchall()
        queries = []
        for row in opt_data:
            instrument = row[instrument_id]
            index = row[index_id]
            symbol = row[symbol_id]
            strike = (row[strike_id])
            expiry = row[expiry_id]
            option_type = row[option_type_id]
            price = row[close_id]
            timestamp = row[timestamp_id]

            key = "%s_%s_%s_%s" % (instrument[3:], symbol, expiry.month, expiry.year)
            try:
                underlying_price = fut_data[key]
                iv, theta, gamma, delta, vega = option_greeks.get_greeks(underlying_price, strike, expiry, option_type,
                                                                         price, timestamp, volatility=0.13)
                update_query = "UPDATE `%s` SET `iv`=%s,`theta`=%s,`gamma`=%s,`delta`=%s,`vega`=%s WHERE id=%d" % (
                    table_name, iv, theta, gamma, delta, vega, index)
                queries.append(update_query)
            except KeyError:
                pass
        insert_data(queries)
        print("Time taken: %s secs" % (time.time() - date_time))
    db_conn.close()


def execute_simple_query(query):
    start_time = time.time()
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db_conn.close()
    print("Query executed in: %s secs" % (time.time() - start_time))
    return result
