import logging
import calendar
from datetime import *
from dateutil import relativedelta

import talib
from talib.abstract import Function
from talib import MA_Type

from model import *

_logger = logging.getLogger('indicator')
month_delta = relativedelta.relativedelta(months=1)
data_min = "data_min"
data_max = "data_max"
pivot_min = "pivot_min"
pivot_max = "pivot_max"

"""
List of Indicators:
1. Momentum - RSI, Stochastic Oscillator
2. Trend - SMA,EMA,MACD
3. Volatility - Bollinger Bands
4. Support and Resistance - Pivot Points
"""


def indicator_info(indicator=""):
    """
    :param indicator:string
    :return: None
    """
    if indicator is "":
        _logger.warning('Enter valid indicator name. For e.g. indicator_info("EMA")')
        _logger.info("For complete list visit http://mrjbq7.github.io/ta-lib/funcs.html")
    else:
        info = Function(indicator).info
        _logger.info(info)


def _check_array(array):
    """
    Check if array has data.
    :param array: list[numeric]
    :return: Boolean
    """
    return (array is None) | (array == [])


def _remove_nan(result):
    """
    Replaces numpy.nan with None value and returns a list.
    Used with rsi, ema, sma, macd, bollinger_bands, stoch
    :param result: numpy.ndarray
    :return: list
    """
    where_are_nan = numpy.isnan(result)
    result[where_are_nan] = None
    result = result.tolist()
    return result


def rsi(array=None, period=14) -> list:
    """
    Calculates Relative Strength Index.
    :param array: list[numeric]
    :param period: int
            Default period = 14
    :return: list
            [double]
    """
    result = []
    indicator_info("RSI")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        array = numpy.asarray(array)
        result = talib.RSI(array, period)
        result = _remove_nan(result)
    _logger.debug('RSI output: %s' % result)
    return result


def stoch(high=None, low=None, close=None, fastk_period=5, fastd_period=3, fastd_matype=MA_Type.SMA) -> dict:
    """
    Calculates Stochastic Oscillator.
    :param high: list[numeric]
    :param low: list[numeric]
    :param close: list[numeric]
    :param fastk_period: int
    :param fastd_period: int
    :param fastd_matype: int
            Moving Average type. Default Moving Average is SMA.
    :return: dict
            {"fastk": list, "fastd": list}
    """
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
        high = numpy.asarray(high)
        low = numpy.asarray(low)
        close = numpy.asarray(close)
        fastk, fastd = talib.STOCHF(high, low, close, fastk_period=fastk_period, fastd_period=fastd_period,
                                    fastd_matype=fastd_matype)
    # _logger.debug('STOCH output slowk: %s ' % slowk)
    # _logger.debug('STOCH output slowd: %s ' % slowd)
    fastk = _remove_nan(fastk)
    fastd = _remove_nan(fastd)
    result = {"fastk": fastk, "fastd": fastd}
    _logger.debug("STOCH output: %s" % result)
    return result


def sma(array=None, period=30) -> list:
    """
    Calculates Simple Moving Average.
    :param array: list[numeric]
    :param period: int
            Default period = 30
    :return: list
            [double]
    """
    result = []
    indicator_info("SMA")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        array = numpy.asarray(array)
        result = talib.SMA(array, timeperiod=period)
        result = _remove_nan(result)
    _logger.debug('SMA output: %s' % result)
    return result


def ema(array=None, period=30) -> list:
    """
    Calculates Exponential Moving Average.
    :param array: list[numeric]
    :param period: int
            Default period = 30
    :return: list
            [double]
    """
    result = []
    indicator_info("EMA")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        array = numpy.asarray(array)
        result = talib.EMA(array, period)
        result = _remove_nan(result)
    _logger.debug('EMA output: %s' % result)
    return result


def macd(array=None, fastperiod=12, slowperiod=26, signalperiod=9) -> dict:
    """
    Calculates Moving Average Convergence/Divergence.
    :param array: list[numeric]
    :param fastperiod: int
    :param slowperiod: int
    :param signalperiod: int
    :return: dict
            {"macd": list, "macdsignal": list, "macdhist": list}
    """
    macd_value, macdsignal, macdhist = [], [], []
    indicator_info("MACD")
    if _check_array(array):
        _logger.warning("Invalid Input")
    elif fastperiod < 1 | slowperiod < 1 | signalperiod < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < fastperiod:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        array = numpy.asarray(array)
        macd_value, macdsignal, macdhist = talib.MACD(array, fastperiod=fastperiod, slowperiod=slowperiod,
                                                      signalperiod=signalperiod)
    macd_value = _remove_nan(macd_value)
    macdsignal = _remove_nan(macdsignal)
    macdhist = _remove_nan(macdhist)
    result = {"macd": macd_value, "macdsignal": macdsignal, "macdhist": macdhist}
    _logger.debug('MACD output: \n      macd: %s \n      macdsignal: %s \n      macdhist: %s' % (
        macd_value, macdsignal, macdhist))
    return result


def bollinger_bands(array=None, timeperiod=5, nbdevup=2, nbdevdn=2, matype=MA_Type.SMA) -> dict:
    """
    Calculates Bollinger Bands for array.
    :param array: list[numeric]
    :param timeperiod: int
    :param nbdevup: int
    :param nbdevdn: int
    :param matype: int
            Moving Average type. Default Moving Average is SMA.
    :return: dict
            {"upperband": list[float], "middleband": list[float], "lowerband": list[float]}
    """
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
        array = numpy.asarray(array)
        upperband, middleband, lowerband = talib.BBANDS(array, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn,
                                                        matype=matype)
    upperband = _remove_nan(upperband)
    middleband = _remove_nan(middleband)
    lowerband = _remove_nan(lowerband)
    result = {"upperband": upperband, "middleband": middleband, "lowerband": lowerband}
    _logger.debug(
        'Bollinger Bands output: \n      UpperBand: %s \n      MiddleBand: %s \n      LowerBand: %s' % (
            upperband, middleband, lowerband))
    return result


def pivot(data=None) -> list:
    """
    Calculates monthly pivot for the given range of data list.
    Formula used is:
    Pivot Point(PP) = (High+low+close)/3
    R1 = 2*PP - low
    S1 = 2*PP - high
    R2 = PP + high-low
    S2 = PP - high-low
    R3 = high + 2*(PP-low)
    S3 = low - 2*(high-PP)
    :param data: list
            [model.DataObject]
    :return: list
            [model.PivotObject]
    """
    period = 30
    if data is None:
        data = []
    pivots = []
    if _check_array(data):
        _logger.warning("Invalid Input")
    else:
        if len(data) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        ranges = _get_ranges(data[0].date, data[len(data) - 1].date)
        pivots = _pivot_data(ranges, data=data)
    return pivots


# This function defines the range for which pivot is to be found
def _get_ranges(min_date, max_date):
    """
    This method finds the different ranges for the pivot calculations
    :param min_date: datetime.date
            This date is minimum date for current data
    :param max_date: datetime.date
            This date is maximum date for current data
    :return: list
            [dict]
    """
    delta = timedelta(days=31)
    diff = max_date - min_date
    ranges = []
    if diff < delta:
        _logger.warning("Pivots can't be found for current data")
    else:
        while min_date <= max_date:
            current_range = _date_ranges(min_date)
            ranges.append(current_range)
            min_date = min_date + month_delta
        # if max_date < min_date:
        #     month_range = _date_ranges(max_date)
        #     ranges.append(month_range)
    return ranges


def _date_ranges(current_date):
    """
    This method returns a dict containing info about pivot dates and data dates
    :param current_date: datetime.date
    :return: dict
            {"data_min": datetime.date, "data_max": datetime.date, "pivot_min": datetime.date,
                  "pivot_max": datetime.date}
    """
    previous_month = current_date - month_delta
    current_range = calendar.monthrange(current_date.year, current_date.month)
    first_pivot_date = date(year=current_date.year, month=current_date.month, day=1)
    last_pivot_date = date(year=current_date.year, month=current_date.month, day=current_range[1])
    previous_range = calendar.monthrange(previous_month.year, previous_month.month)
    data_start = date(year=previous_month.year, month=previous_month.month, day=1)
    data_end = date(year=previous_month.year, month=previous_month.month, day=previous_range[1])
    date_range = {data_min: data_start, data_max: data_end, pivot_min: first_pivot_date,
                  pivot_max: last_pivot_date}
    _logger.debug(date_range)
    return date_range


def _pivot_data(date_range, data):
    """
    This method is used to get the pivot data for a range of date values.
    In this method, pivot_min and pivot_max are dates for which pivot is to be found.
    data_min and data_max are the data value range required for the current pivot
    :param date_range: dict
                    {"data_min": datetime.date, "data_max": datetime.date, "pivot_min": datetime.date,
                  "pivot_max": datetime.date}
    :param data: list
            [model.DataObject]
    :return: list
            [model.PivotObject]
    """
    data_pivot = []
    for kRange in date_range:
        _logger.debug("Pivot values for the range %s and %s" % (kRange[pivot_min], kRange[pivot_max]))
        pivot_values = _get_pivot_for_range(kRange[data_min], kRange[data_max], data)
        _logger.debug(pivot_values)
        for i in range(len(data)):
            current_date = data[i].date
            if kRange[pivot_min] <= current_date <= kRange[pivot_max]:
                # data_and_pivot = [data[i], pivot_values]
                data_and_pivot = pivot_values
                data_pivot.append(data_and_pivot)
    _logger.debug(data_pivot)
    return data_pivot


def _get_pivot_for_range(min_date, max_date, data):
    """
    This method extracts data for pivot calculation from the data list
    and returns the result in PivotObject
    :param min_date: datetime.date
    :param max_date: datetime.date
    :param data: list
            [model.DataObject]
    :return: model.PivotObject
    """
    high, low, close = [], [], []
    for i in range(len(data)):
        current_date = data[i].date
        if min_date <= current_date <= max_date:
            high.append(data[i].high)
            low.append(data[i].low)
            close.append(data[i].close)
    pivot_values = _calc_pivot_points(high, low, close)
    return pivot_values


def _calc_pivot_points(high, low, close):
    """
    This method calculates the pivot points for the given params
    :param high: list
    :param low: list
    :param close: list
    :return: model.PivotObject
    """
    result = PivotObject()
    if (high != []) & (low != []) & (close != []):
        highest_high = max(high)
        lowest_low = min(low)
        last_close = close[len(close) - 1]
        _logger.debug("High for period: %s" % highest_high)
        _logger.debug("Low for period: %s" % lowest_low)
        _logger.debug("Close for the period: %s" % last_close)
        pp = (highest_high + lowest_low + last_close) / 3
        r1 = (2 * pp) - lowest_low
        s1 = (2 * pp) - highest_high
        r2 = pp + (highest_high - lowest_low)
        s2 = pp - (highest_high - lowest_low)
        r3 = highest_high + (2 * (pp - lowest_low))
        s3 = lowest_low - (2 * (highest_high - pp))
        result = PivotObject(pp=pp, r1=r1, r2=r2, r3=r3, s1=s1, s2=s2, s3=s3)
    return result
