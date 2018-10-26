import csv
import os
import shutil
import time
import zipfile
from datetime import datetime, date

from options import database_connection

extract_dir = 'extracted/'
default_path = 'C:/Users/sb/Downloads/niftyoptionsdata/'
header = "INSERT INTO `%s`(`instrument`, `symbol`, `expiry`, `strike`, `option_typ`, `open`, `high`, `low`, " \
         "`close`, `settle_pr`, `contracts`, `val`, `open_int`, `chg_in_oi`, `timestamp`) VALUES " % database_connection.table_name
delimiter = ','


def _extract_files(path: str):
    """
    This is used to extract the zip files in a directory
    :param path: Path to firectory with zip files
    :return: None
    """
    extract_path = path + extract_dir
    if os.path.isdir(extract_path):
        shutil.rmtree(extract_path)
        print('Deleted %s' % extract_dir)

    dir_contents = os.walk(path)
    files = []
    for dirpath, dirnames, filenames in dir_contents:
        files += filenames
    print("Total files: %s" % len(files))

    for zip_file in files:
        file_path = path + zip_file
        if zipfile.is_zipfile(file_path):
            zp = zipfile.ZipFile(file_path)
            print("Extracting: %s" % zip_file)
            zp.extractall(extract_path)


def _read_data(path: str):
    """
    This is used to read the csv file i.e. FO bhavcopy
    :param path: str
        Path to the csv file
    :return: None
    """
    extract = path + extract_dir

    csv_files = os.listdir(extract)
    for csv_file_name in csv_files:
        queries = []
        csv_path = extract + csv_file_name
        print("Reading: %s" % csv_path)
        # f = open(csv_path, newline='')
        # csv_reader = csv.reader(f, delimiter=' ', quotechar="|")
        f = open(csv_path)
        csv_reader = csv.reader(f)
        file_start_time = time.time()
        for row in csv_reader:
            trailer = _read_row(row)
            if trailer is not None:
                queries.append(header + trailer)
        f.close()
        print("Time taken to read file: %s seconds" % (time.time() - file_start_time))
        db_start_time = time.time()
        database_connection.insert_data(queries)
        print("Queries executed: %s" % len(queries))
        print("Time taken to  execute queries: %s seconds" % (time.time() - db_start_time))


def _read_row(row):
    """
    It is used to read the row in the csv file for the database insertion
    :param row: list
            Values of the row in a list
    :return: str
            Values for the database query
    """
    data_arr = row
    instrument = data_arr[0]
    if instrument != 'INSTRUMENT':
        symbol = data_arr[1]
        # expiry = data_arr[2]
        expiry = (datetime.strptime(data_arr[2], "%d-%b-%Y")).strftime("%Y-%m-%d")
        strike = data_arr[3]
        if strike == 'XX':
            strike = float(0)
        else:
            strike = float(strike)
        option_typ = data_arr[4]
        open_price = float(data_arr[5])
        high = float(data_arr[6])
        low = float(data_arr[7])
        close = float(data_arr[8])
        settle_pr = float(data_arr[9])
        contracts = int(data_arr[10])
        val = float(data_arr[11])
        open_int = int(data_arr[12])
        chg_in_oi = int(data_arr[13])
        timestamp = (datetime.strptime(data_arr[14], "%d-%b-%Y")).strftime("%Y-%m-%d")
        trailer = "('%s','%s', '%s', %d,'%s', %f, %f, %f, %f, %f, %d, %f, %d, %d, '%s');" % (
            instrument, symbol, expiry, strike, option_typ, open_price, high, low, close, settle_pr, contracts,
            val, open_int, chg_in_oi, timestamp)
        return trailer
    else:
        return None


def insert_bulk_data(path: str = None, truncate: bool = True):
    """
    This used to insert bhavcopy in bulk into the database
    :param path: str
            Path to the folder containing all the bhavcopy zip files to be inserted into database
    :param truncate: bool
            If table is already present then truncate if True.
    :return: None
    """
    if path is not None:
        path = default_path
        start_time = time.time()
        print("Bulk entries started...")
        _extract_files(path)
        database_connection.bulk_entries(truncate)
        _read_data(path)
        print("Total time taken to execute bulk entries: %s seconds" % (time.time() - start_time))
    else:
        print('No path specified')
        print(path)


def insert_bhavcopy(path: str, filename: str, ):
    """
    Used to insert the bhavcopy into the database
    :param path: str
            Path to the directory where file is located
    :param filename: str
            Name of the file i.e. bhavcopy zip file
    :return: None
    """
    zip_path = path + filename
    if zipfile.is_zipfile(zip_path):
        queries = []
        zp = zipfile.ZipFile(zip_path)
        csv_name = zp.namelist()[0]
        csv_file = path + csv_name
        if not os.path.isfile(csv_file):
            print("Extracting...%s" % csv_file)
            zp.extractall(path)
        f = open(csv_file)
        csv_reader = csv.reader(f)
        for rows in csv_reader:
            trailer = _read_row(rows)
            if trailer is not None:
                queries.append(header + trailer)
        database_connection.insert_data(queries)
    else:
        print("Not a zip file")
        print(zip_path)


def update_option_greeks(timestamp: date = None):
    """
    It is used to update the option greeks in the database.
    :param timestamp: date
            It is to update greeks for a particular date.
            If None, greeks are updated for whole database
    :return: None
    """
    start_time = time.time()
    # if timestamp is None:
    #     database_con/nection.add_greeks_column()
    database_connection.add_greeks_column()
    database_connection.update_database_greeks(timestamp)
    print("Total Time Taken: %s" % (time.time() - start_time))
