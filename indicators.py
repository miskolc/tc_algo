import logging

import talib
from talib.abstract import Function
from talib import MA_Type
import numpy

_logger = logging.getLogger('indicator')


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


# # Pivot Points
# Pivot Point(PP) = (High+low+close)/3
# R1 = 2*PP - low
# S1 = 2*PP - high
# R2 = PP + high-low
# S2 = PP - high-low
# R3 = high + 2*(PP-low)
# S3 = low - 2*(high-PP)
def pivot(high=None, low=None, close=None, period=10):
    result = []
    if _check_array(high) | _check_array(low) | _check_array(close):
        _logger.warning("Invalid Input")
    elif (len(high) != len(low)) | (len(high) != len(close)):
        _logger.warning("Data length differs")
    else:
        if len(high) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        result = 4
    _logger.debug(' output: %s' % result)
    return result
