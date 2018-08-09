import logging
from datetime import *

import numpy
import quandl

import api
from model import *

_logger = logging.getLogger("data_parser")


def get_date_ohlc(symbol=api.nifty50, start_date=api.start_date, end_date=""):
    data = get_data(symbol=symbol, start_date=start_date, end_date=end_date)
    date_values = get_date(data)
    open = get_open(data)
    high = get_high(data)
    low = get_low(data)
    close = get_close(data)
    ohlc = {"symbol": symbol, "date": date_values, "open": open, "high": high, "low": low, "close": close}
    return ohlc


def get_data(symbol=api.nifty50, start_date=api.start_date, end_date=""):
    data = []
    quandl.ApiConfig.api_key = api.quandl_api_key
    response = quandl.get(symbol, returns="numpy", start_date=start_date, end_date=end_date)
    for i in range(len(response)):
        item = response[i]
        data.append(DataObject(item))
    # _logger.debug("%s" % data)
    return data


# Input should be of List[DataObject]
def get_date(data=None):
    date_arr = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.date
            date_arr.append(value)
    # date_arr = date_format(date_arr)
    return date_arr


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


# Required when data is in UNIX timestamp
def current_month(timestamp=""):
    current = date.fromtimestamp(float(timestamp))
    # date1 = date(year=2018, month=1, day=15)
    # delta = relativedelta.relativedelta(month=1)
    # old = current - delta
    # test = date(year=2018, month=7, day=15)
    # print(date2 < test < date1)
    return current.month


def data_builder(data, **kwargs):
    father = []
    params = ["date", "open", "high", "low", "close", "volume"]
    keys_index = 0
    keys = []
    for key, value in kwargs.items():
        keys.append(key)
    father = _append_data(data)
    indicators = []
    values = kwargs.values()
    for item in values:
        if type(item) == list:
            _logger.debug("list")
            # indicators.append(item)
            params.append(keys[keys_index])
            keys_index += 1
        elif type(item) == dict:
            _logger.debug('dict')
            for key, value in item.items():
                params.append(keys[keys_index] + "_" + key)
            dict_values = item.values()
            for child in dict_values:
                indicators.append(child)
            keys_index += 1
        else:
            _logger.warning("Unknown data format or type")
    father = _append_indicators(indicators, father)
    _logger.debug("Params are: %s" % params)
    result = [params]
    for item in father:
        result.append(item)
    return result


def _append_data(data):
    result = []
    for child in data:
        grand_child = [child.date, child.open, child.high, child.low, child.close, child.volume]
        result.append(grand_child)
    return result


def _append_indicators(indicators, father):
    for item in indicators:
        # _logger.debug(len(father))
        # _logger.debug(len(item))
        for i in range(len(father)):
            # if type(item[i]) == PivotObject:
            #     pv = item[i]
            #     item[i] = [pv.pp, pv.r1, pv.r2, pv.r3, pv.s1, pv.s2, pv.s3]
            #     father[i] += item[i]
            # else:
            father[i].append(item[i])
    return father
