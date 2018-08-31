import logging
import calendar
from datetime import *
from dateutil.relativedelta import relativedelta

import talib
from talib.abstract import Function
# noinspection PyProtectedMember
from talib import MA_Type

import data_parser
from model import *

_logger = logging.getLogger('indicators')
day_delta = relativedelta(days=1)
week_delta = relativedelta(weeks=1)
month_delta = relativedelta(months=1)


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
        _logger.info(Function(indicator).info)


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
    indicator_info(Keys.rsi)
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
    indicator_info(Keys.stoch)
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
    result = {Keys.fastk: fastk, Keys.fastd: fastd}
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
    indicator_info(Keys.sma)
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
    indicator_info(Keys.ema)
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
    indicator_info(Keys.macd)
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
    result = {Keys.macd_value: macd_value, Keys.macdsignal: macdsignal, Keys.macdhist: macdhist}
    _logger.debug('MACD output: \n      macd_value: %s \n      macdsignal: %s \n      macdhist: %s' % (
        macd_value, macdsignal, macdhist))
    return result


def bollinger_bands(array=None, timeperiod=5, nbdevup=2, nbdevdn=2, matype=MA_Type.SMA) -> dict:
    """
    Calculates Bollinger Bands for array.
    :param array: list[numeric]
    :param timeperiod: int
    :param nbdevup: int
            Upper deviation
    :param nbdevdn: int
            Lower deviation
    :param matype: int
            Moving Average type. Default Moving Average is SMA.
    :return: dict
            {"upperband": list[float], "middleband": list[float], "lowerband": list[float]}
    """
    upperband, middleband, lowerband = [], [], []
    indicator_info(Keys.bbands)
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
    result = {Keys.upperband: upperband, Keys.middleband: middleband, Keys.lowerband: lowerband}
    _logger.debug(
        'Bollinger Bands output: \n      UpperBand: %s \n      MiddleBand: %s \n      LowerBand: %s' % (
            upperband, middleband, lowerband))
    return result


def pivot(data=None, interval: str = Keys.monthly, charts=True):
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
    :param interval: str
            Interval for which pivots needed.
            Currently supports daily, weekly and monthly pivots.
    :param charts: Boolean
                Whether data is required for the charts. If false data is returned in list[PivotObject]

    :return: dict
            dict(pp=list[double], r1=list[double], r2=list[double], r3=list[double],
                                        s1=list[double], s2=list[double], s3=list[double])
                or
            list[PivotObject]

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
        if interval == Keys.daily:
            ranges = _get_daily_ranges(data)
            pivots = _pivot_data(ranges, data=data)
        else:
            if interval == Keys.weekly:
                ranges = _get_weekly_ranges(data[0].date, data[len(data) - 1].date)
            else:
                ranges = _get_monthly_ranges(data[0].date, data[len(data) - 1].date)
            pivots = _pivot_data(ranges, data=data)

    pp, r1, r2, r3, s1, s2, s3 = [], [], [], [], [], [], []
    for item in pivots:
        pp.append(item.pp)
        r1.append(item.r1)
        r2.append(item.r2)
        r3.append(item.r3)
        s1.append(item.s1)
        s2.append(item.s2)
        s3.append(item.s3)
    result = {Keys.pp: pp,
              Keys.r1: r1,
              Keys.r2: r2,
              Keys.r3: r3,
              Keys.s1: s1,
              Keys.s2: s2,
              Keys.s3: s3}
    if charts:
        return result
    else:
        return pivots


def _get_daily_ranges(data: list):
    """
    This method finds the daily ranges for the pivot calculations
    :param: list[DataObject]
    :return: list
            [dict]
    """
    ranges = []
    for i in range(len(data)):
        if i == 0:
            data_min = data_max = data[i].date - timedelta(days=1)
            pivot_min = pivot_max = data[i].date
        else:
            data_min = data_max = data[i - 1].date
            pivot_min = pivot_max = data[i].date
        date_range = {Keys.data_min: data_min, Keys.data_max: data_max, Keys.pivot_min: pivot_min,
                      Keys.pivot_max: pivot_max}
        ranges.append(date_range)
        i += 1
    return ranges


def _get_weekly_ranges(min_date, max_date):
    """
    This method finds the weekly ranges for the pivot calculations
    :param min_date: datetime.date
            This date is minimum date for current data
    :param max_date: datetime.date
            This date is maximum date for current data
    :return: list
            [dict]
    """
    delta = timedelta(days=7)
    diff = max_date - min_date
    ranges = []
    if diff < delta:
        _logger.warning("Pivots can't be found for current data")
    else:
        while min_date < max_date:
            current_range = _get_date_ranges(min_date, interval=Keys.weekly)
            ranges.append(current_range)
            min_date = min_date + week_delta
        if (max_date < min_date) & (max_date.isocalendar()[1] == min_date.isocalendar()[1]):
            month_range = _get_date_ranges(max_date, interval=Keys.weekly)
            ranges.append(month_range)
    return ranges


def _get_monthly_ranges(min_date, max_date):
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
            current_range = _get_date_ranges(min_date, interval=Keys.monthly)
            ranges.append(current_range)
            min_date = min_date + month_delta
    return ranges


def _get_date_ranges(current_date, interval: str):
    """
    This method returns a dict containing info about pivot dates and data dates
    :param current_date: datetime.date
    :return: dict
            {"data_min": datetime.date, "data_max": datetime.date, "pivot_min": datetime.date,
                  "pivot_max": datetime.date}
    """
    if interval == Keys.weekly:
        weekday = current_date.isocalendar()
        back_time = timedelta(days=weekday[2] - 1)
        forward_time = timedelta(days=6)
        week_first = current_date - back_time
        week_last = week_first + forward_time
        previous_week_first = week_first - timedelta(days=7)
        previous_week_last = week_first - timedelta(days=1)
        date_range = {Keys.data_min: previous_week_first, Keys.data_max: previous_week_last, Keys.pivot_min: week_first,
                      Keys.pivot_max: week_last}
        _logger.debug(date_range)
        return date_range
    if interval == Keys.monthly:
        previous_month = current_date - month_delta
        current_range = calendar.monthrange(current_date.year, current_date.month)
        first_pivot_date = date(year=current_date.year, month=current_date.month, day=1)
        last_pivot_date = date(year=current_date.year, month=current_date.month, day=current_range[1])
        previous_range = calendar.monthrange(previous_month.year, previous_month.month)
        data_start = date(year=previous_month.year, month=previous_month.month, day=1)
        data_end = date(year=previous_month.year, month=previous_month.month, day=previous_range[1])
        date_range = {Keys.data_min: data_start, Keys.data_max: data_end, Keys.pivot_min: first_pivot_date,
                      Keys.pivot_max: last_pivot_date}
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
        _logger.debug("Pivot values for the range %s and %s" % (kRange[Keys.pivot_min], kRange[Keys.pivot_max]))
        pivot_values = _get_pivot_for_range(kRange[Keys.data_min], kRange[Keys.data_max], data)
        _logger.debug(pivot_values)
        for i in range(len(data)):
            current_date = data[i].date
            if kRange[Keys.pivot_min] <= current_date <= kRange[Keys.pivot_max]:
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
        pp = data_parser.round_float((highest_high + lowest_low + last_close) / 3.0)
        r1 = data_parser.round_float((2.0 * pp) - lowest_low)
        s1 = data_parser.round_float((2.0 * pp) - highest_high)
        r2 = data_parser.round_float(pp + (highest_high - lowest_low))
        s2 = data_parser.round_float(pp - (highest_high - lowest_low))
        r3 = data_parser.round_float(highest_high + (2.0 * (pp - lowest_low)))
        s3 = data_parser.round_float(lowest_low - (2.0 * (highest_high - pp)))
        result = PivotObject(pp=pp, r1=r1, r2=r2, r3=r3, s1=s1, s2=s2, s3=s3)
    return result


def _check_array(array):
    """
    Check if array has data.
    :param array: list[numeric]
    :return: Boolean
    """
    return (array is None) | (array == [])


def _remove_nan(result):
    """
    Replaces numpy.nan with default value and returns a list.
    Used with rsi, ema, sma, macd, bollinger_bands, stoch (talib functions)
    :param result: numpy.ndarray
    :return: list
    """
    result = result.tolist()
    for i in range(len(result)):
        if numpy.isnan(result[i]):
            result[i] = ct.default
    for i in range(len(result)):
        if result[i] == ct.default:
            pass
        else:
            result[i] = float(Decimal(result[i]).quantize(PRECISION))
    return result
