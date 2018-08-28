"""
This file contains the API related info and constants which can be used.
For complete list of symbols visit: https://www.quandl.com/data/NSE-National-Stock-Exchange-of-India
"""
from model import Symbol

quandl_api_key = "y4jybLNT_iLmo_jJMfae"
link = "https://www.quandl.com/api/v3/datasets/NSE/CNX_NIFTY.json?api_key=y4jybLNT_iLmo_jJMfae"

min_date = "03-07-1990"


class NSECM:
    HDFCBANK = Symbol("HDFCBANK", "NSE/HDFCBANK", 1)


class NSEFO:
    NIFTY50 = Symbol("NIFTY50", "NSE/CNX_NIFTY", 75)
