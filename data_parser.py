import logging

import api
from model import DataObject
import quandl

_logger = logging.getLogger("data_parser")


def get_ohlc(symbol="NSE/CNX_NIFTY", start_date="03-07-1990", end_date=""):
    data = get_data(symbol=symbol, start_date=start_date, end_date=end_date)
    open = get_open(data)
    high = get_high(data)
    low = get_low(data)
    close = get_close(data)
    ohlc = {"open": open, "high": high, "low": low, "close": close}
    return ohlc


def get_data(symbol="NSE/CNX_NIFTY", start_date="03-07-1990", end_date=""):
    data = []
    quandl.ApiConfig.api_key = api.quandl_api_key
    response = quandl.get(symbol, returns="numpy", start_date=start_date, end_date=end_date)
    for i in range(len(response)):
        item = response[i]
        data.append(DataObject(item))
    return data


def get_date(data=None):
    date = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.date
            date.append(value)
    return date


def get_open(data=None):
    open = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.open
            open.append(value)
    return open


def get_high(data=None):
    high = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.high
            high.append(value)
    return high


def get_low(data=None):
    low = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.low
            low.append(value)
    return low


def get_close(data=None):
    close = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.close
            close.append(value)
    return close


def get_volume(data=None):
    volume = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.volume
            volume.append(value)
    return volume


def get_turnover(data=None):
    turnover = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.turnover
            turnover.append(value)
    return turnover
