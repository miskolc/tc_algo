import time
from datetime import date

import mysql.connector

from options import option_greeks
from constants import DbIndex

host = 'localhost'
user = 'root'
password = ''

db_name = 'fo'
table_name = 'fo_data'
interest = 0.0

columns = ['id', 'instrument', 'symbol', 'expiry', 'strike', 'option_typ', 'open', 'high', 'low', 'close', 'settle_pr',
           'contracts', 'val', 'open_int', 'chg_in_oi', 'timestamp', 'iv', 'theta', 'gamma', 'delta', 'vega']


def _check_database():
    """
    This checks for the for the database present in the MySQL server. If not then it creates the database.
    :return: None
    """
    conn = mysql.connector.connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'" % db_name
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        query = "CREATE DATABASE IF NOT EXISTS %s" % db_name
        cursor.execute(query)
        print("Database created: %s" % db_name)
    else:
        print("Database already present")

    cursor.close()
    conn.close()


def _check_table(truncate: bool):
    """
    This checks for the table in the database. If not present then it creates the table.
    :param truncate:
    :return: None
    """
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
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
    """
    This is used to enter multiple queries into the database.
    :param queries: List[str]
            It should the a list of queries in str format which can be inserted directly in database.
    :return: None
    """
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    for query in queries:
        cursor.execute(query)
    db_conn.commit()
    cursor.close()
    db_conn.close()


def bulk_entries(truncate: bool):
    """
    This is used to check resources before inserting bulk entries into the database
    :param truncate: bool
            If table is already present then truncate if True.
    :return: None
    """
    _check_database()
    _check_table(truncate)


def add_greeks_column():
    """
    This checks and adds greeks columns to the database i.e. iv, theta, gamma, delta and vega.
    :return: None
    """
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


def _get_fut_data(timestamp: str):
    """
    This returns the Futures data for the timestamp given as input.
    :param timestamp: str
            It is the timestamp for which futures data is required.
            Format e.g. '2018-10-25'
    :return: dict
            Key is of the type 'instrument_symbol_month_year' e.g. 'IDX_NIFTY_10_18'.
            Value is the close price of the future on the input timestamp.
    """
    data = {}
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    underlying_query = "SELECT * FROM %s WHERE instrument LIKE 'FUT%%' AND timestamp = '%s'" % (table_name, timestamp)
    cursor.execute(underlying_query)
    fut_data = cursor.fetchall()
    for fut in fut_data:
        instrument = fut[DbIndex.instrument_id.value]
        symbol = fut[DbIndex.symbol_id.value]
        expiry = fut[DbIndex.expiry_id.value]
        close = fut[DbIndex.close_id.value]
        key = "%s_%s_%s_%s" % (instrument[3:], symbol, expiry.month, expiry.year)
        data.update({key: close})
    db_conn.close()
    return data


def update_database_greeks(ts: date):
    """
    This updates the greeks for the given timestamp and insert them in database.
    :param ts: date
            Timestamp for which the greeks are to be updated
    :return: None
    """
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    if ts is not None:
        timestamp_query = "SELECT distinct timestamp from %s where timestamp = '%s-%s-%s' ORDER BY timestamp ASC " % (
            table_name, ts.year, ts.month, ts.day)
    else:
        timestamp_query = 'SELECT distinct timestamp from %s ORDER BY timestamp ASC' % table_name

    cursor.execute(timestamp_query)
    x = cursor.fetchall()
    for obs_ts in x:
        date_time = time.time()
        data_date = obs_ts[0]
        print("Updating options data for: %s" % data_date)
        fut_data = _get_fut_data(data_date)
        opt_query = "SELECT * FROM `%s` WHERE instrument LIKE 'OPT%%' AND timestamp='%s' ORDER BY id ASC " % (
            table_name, data_date)
        cursor.execute(opt_query)
        opt_data = cursor.fetchall()
        queries = []
        for row in opt_data:
            instrument = row[DbIndex.instrument_id.value]
            index = row[DbIndex.index_id.value]
            symbol = row[DbIndex.symbol_id.value]
            strike = (row[DbIndex.strike_id.value])
            expiry = row[DbIndex.expiry_id.value]
            option_type = row[DbIndex.option_type_id.value]
            price = row[DbIndex.close_id.value]
            timestamp = row[DbIndex.timestamp_id.value]

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
    """
    This used to execute a MySQL query in the database.
    :param query: str
            MySQL query to be executed
    :return: None
    """
    start_time = time.time()
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db_conn.close()
    print("Query executed in: %s secs" % (time.time() - start_time))
    return result
