import time
# import urllib
from urllib import request
from datetime import date
import pandas as pd

from options import database_connection as dbc

columns = ['id', 'instrument', 'symbol', 'expiry', 'strike', 'option_typ', 'open', 'high', 'low', 'close', 'settle_pr',
           'contracts', 'val', 'open_int', 'chg_in_oi', 'timestamp', 'iv', 'theta', 'gamma', 'delta', 'vega']


def symbol_data(symbol, obs_date: str, expiry_date: str):
    # call_query = "Select close, iv, delta, gamma, vega, theta from %s where symbol='%s' and instrument like 'OPT%%' " % (
    call_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' " % (dbc.table_name, symbol,)
    # print(call_query)
    call_data = dbc.execute_simple_query(call_query)
    # print(call_data)
    return call_data


# download_url = 'https://www.nseindia.com/content/historical/DERIVATIVES/2018/OCT/fo23OCT2018bhav.csv.zip'


if __name__ == '__main__':
    start_time = time.time()
    data = symbol_data("NIFTY", "2018-10-22", "2018-10-25")
    df = pd.DataFrame(data, columns=columns)
    print(df.__len__())
    x = df.query("expiry == '2018-10-25'")
    print(x)
    # print(df)
    # print(df[df['expiry'] == date(2018,10,23)])
    # print(df[df['timestamp'] == date(2018, 10, 22)])
    # print(df[(df['option_typ'] == 'CE')])
    print("Time: %s" % (time.time() - start_time))
