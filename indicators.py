import logging
from datetime import *

import talib
from talib.abstract import Function
from talib import MA_Type
import numpy

import data_parser
from model import *

_logger = logging.getLogger('indicator')
month_delta = timedelta(days=31)


# TODO: List of Indicators:
# TODO: 1. Momentum - RSI, Stochastic Oscillator
# TODO: 2. Trend - SMA,EMA,MACD
# TODO: 3. Volatility - Bollinger Bands
# TODO: 4. Support and Resistance - Pivot Points
# Declaration, info, check, result

# Get info for the required function in ta-lib
def indicator_info(indicator=""):
    if indicator is "":
        _logger.warning('Enter valid indicator name. For e.g. indicator_info("EMA")')
        _logger.info("For complete list visit http://mrjbq7.github.io/ta-lib/funcs.html")
    else:
        info = Function(indicator).info
        _logger.info(info)


def _check_array(array):
    return (array is None) | (array == [])


# Simple moving average. Default period = 30
def _remove_nan(result):
    where_are_nan = numpy.isnan(result)
    result[where_are_nan] = 0
    return result


# Relative Strength Index. Default period = 14
def rsi(array=None, period=14):
    result = []
    indicator_info("RSI")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        result = talib.RSI(array, period)
        result = _remove_nan(result)
    _logger.debug('RSI output: %s' % result)
    return result


# Stochastic Oscillator. Default Moving Average is SMA.
def stoch(high=None, low=None, close=None, fastk_period=5, fastd_period=3, fastd_matype=MA_Type.SMA):
    fastk, fastd = [], []
    indicator_info("STOCH")
    if _check_array(high) | _check_array(low) | _check_array(close):
        _logger.warning("Invalid Input")
    elif (len(high) != len(low)) | (len(high) != len(close)):
        _logger.warning("Data length differs")
    elif fastk_period < 1 | fastd_period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(high) < fastk_period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        fastk, fastd = talib.STOCHF(high, low, close, fastk_period=fastk_period, fastd_period=fastd_period,
                                    fastd_matype=fastd_matype)
    # _logger.debug('STOCH output slowk: %s ' % slowk)
    # _logger.debug('STOCH output slowd: %s ' % slowd)
    result = {"fastk": fastk, "fastd": fastd}
    _logger.debug("STOCH output: %s" % result)
    return result


# Simple Moving Average. Default period = 30
def sma(array=None, period=30):
    result = []
    indicator_info("SMA")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        result = talib.SMA(array, period)
        result = _remove_nan(result)
    _logger.debug('SMA output: %s' % result)
    return result


# Exponential Moving Average. Default period = 30
def ema(array=None, period=30):
    result = []
    indicator_info("EMA")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        result = talib.EMA(array, period)
        result = _remove_nan(result)
    _logger.debug('EMA output: %s' % result)
    return result


# Moving Average Convergence/Divergence
def macd(array=None, fastperiod=12, slowperiod=26, signalperiod=9):
    macd_value, macdsignal, macdhist = [], [], []
    indicator_info("MACD")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif fastperiod < 1 | slowperiod < 1 | signalperiod < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < fastperiod:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        macd_value, macdsignal, macdhist = talib.MACD(array, fastperiod=fastperiod, slowperiod=slowperiod,
                                                      signalperiod=signalperiod)
    result = {"macd": macd_value, "macdsignal": macdsignal, "macdhist": macdhist}
    _logger.debug('MACD output: %s' % result)
    return result


# Bollinger Bands. Default Moving Average is SMA
def bollinger_bands(array=None, timeperiod=5, nbdevup=2, nbdevdn=2, matype=MA_Type.SMA):
    upperband, middleband, lowerband = [], [], []
    indicator_info("BBANDS")
    if (array is None) | (array == []):
        _logger.warning("Invalid Input")
    elif timeperiod < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if (nbdevdn < 0) | (nbdevup < 0):
            _logger.warning("Deviation is negative")
        if len(array) < timeperiod:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        upperband, middleband, lowerband = talib.BBANDS(array, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn,
                                                        matype=matype)
    result = {"upperband": upperband, "middleband": middleband, "lowerband": lowerband}
    _logger.debug('Bollinger Bands output: %s' % result)
    return result


# Pivot Points
# Monthly Pivot only
# Pivot Point(PP) = (High+low+close)/3
# R1 = 2*PP - low
# S1 = 2*PP - high
# R2 = PP + high-low
# S2 = PP - high-low
# R3 = high + 2*(PP-low)
# S3 = low - 2*(high-PP)
def pivot(data=None, period=10) -> dict:
    if data is None:
        data = {}
    pivots = []
    date_list = data['date']
    if _check_array(date_list):
        _logger.warning("Invalid Input")
    else:
        if len(date_list) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        ranges = _get_ranges(date_list[0], date_list[len(date_list) - 1], data=data)
        for i in ranges:
            pivots += _pivot_data(i['pivot_min'], i['pivot_max'], data=data)
    _logger.debug('Actual data is: %s' % data)
    final = {"date": data['date'], 'pivot': pivots}
    _logger.debug('Pivot output: %s' % final)
    return final


# This function defines the range for which pivot is to be found
def _get_ranges(min_date, max_date, data=dict):
    diff = max_date - min_date
    result = []
    if diff < month_delta:
        _logger.warning("Pivots can't be found for current data")
    else:
        while max_date > min_date:
            date_range = _pivot_date_range(max_date)
            # result.append(_pivot_data(date_range['pivot_min'], date_range['pivot_max'], data))
            result.append(date_range)
            max_date = date_range['pivot_max']
    return result


# current_date should be in datetime.date format
def _pivot_date_range(current_date):
    previous = current_date - month_delta
    first_date = date(year=previous.year, month=previous.month, day=1)
    first_day_current = date(year=current_date.year, month=current_date.month, day=1)
    time_delta = timedelta(days=1)
    last_date = first_day_current - time_delta
    return {"pivot_min": first_date, "pivot_max": last_date}


# This returns pivot for a range of dates
def _pivot_data(pivot_min, pivot_max, data):
    high, low, close = [], [], []
    for i in range(len(data['date'])):
        input_date = data['date'][i]
        if pivot_min <= input_date <= pivot_max:
            high.append(data['high'][i])
            low.append(data['low'][i])
            close.append(data['close'][i])
    length = len(high)
    pivot = _calc_pivot_points(high, low, close)
    # _logger.debug("%s" % pivot)
    pivot_arr = []
    for i in range(length):
        pivot_arr.append(pivot)
    # _logger.debug(pivot_arr)
    return pivot_arr


def _calc_pivot_points(high, low, close):
    result = PivotObject()
    if (high != []) & (low != []) & (close != []):
        highest_high = max(high)
        lowest_low = min(low)
        last_close = close[len(close) - 1]
        pp = (highest_high + lowest_low + last_close) / 3
        r1 = 2 * pp - lowest_low
        s1 = 2 * pp - highest_high
        r2 = pp + (highest_high - lowest_low)
        s2 = pp - (highest_high - lowest_low)
        r3 = highest_high + 2 * (pp - lowest_low)
        s3 = lowest_low - 2 * (highest_high - pp)
        result = PivotObject(pp=pp, r1=r1, r2=r2, r3=r3, s1=s1, s2=s2, s3=s3)
    return result
