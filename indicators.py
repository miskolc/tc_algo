import logging

import talib
from talib.abstract import Function
import numpy

_logger = logging.getLogger('indicator')


# TODO: List of Indicators:
# TODO: 1. Momentum - RSI, Stochastic Oscillator
# TODO: 2. Trend - SMA,EMA,MACD
# TODO: 3. Volatility - Bollinger Bands
# TODO: 4. Support and Resistance - Pivot Points


# Get info for the required function in ta-lib
def indicator_info(indicator=""):
    if indicator is "":
        _logger.warning('Enter valid indicator name. For e.g. indicator_info("EMA")')
        _logger.info("For complete list visit http://mrjbq7.github.io/ta-lib/funcs.html")
    else:
        info = Function(indicator).info
        _logger.info(info)


# Simple moving average. Default period = 30
def remove_nan(result):
    where_are_nan = numpy.isnan(result)
    result[where_are_nan] = 0
    return result


# Relative Strength Index. Default period = 14
def rsi(array=None, period=14):
    result = []
    if (array is None) | (array == []):
        _logger.warning("Invalid Input")
    else:
        if period < 1:
            _logger.warning("Period should be greater than 0")
        else:
            if len(array) < period:
                _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
            result = talib.RSI(array, period)
            result = remove_nan(result)
        _logger.debug('RSI output: %s' % result)
    return result


# Stochastic Oscillator. 
def stoch(high=None, low=None, close=None, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3,
          slowd_matype=0):
    result = []
    if (high is None) | (high == []):
        _logger.warning("Invalid Input")
    else:
        if fastk_period < 1:
            _logger.warning("Period should be greater than 0")
        else:
            if len(high) < fastk_period:
                _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
            result = talib.STOCH(high, low, close, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype)
        _logger.debug('STOCH output: %s' % result)
    return result


# Simple Moving Average. Default period = 30
def sma(array=None, period=30):
    result = numpy.ndarray
    if array is None:
        array = []
    if period < 1:
        _logger.warning("Period should be greater than 0")
    else:
        if len(array) < period:
            _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
        result = talib.SMA(array, period)
        result = remove_nan(result)
    _logger.debug('SMA output: %s' % result)
    return result


# Exponential Moving Average. Default period = 30
def ema(array=None, period=30):
    result = []
    if (array is None) | (array == []):
        _logger.warning("Invalid Input")
    else:
        if period < 1:
            _logger.warning("Period should be greater than 0")
        else:
            if len(array) < period:
                _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
            result = talib.EMA(array, period)
            result = remove_nan(result)
        _logger.debug('EMA output: %s' % result)
    return result


# Rate of Change. Default period = 10
def roc(array=None, period=10):
    result = numpy.ndarray
    if (array is None) | (array == []):
        _logger.warning("Invalid Input")
    else:
        if period < 1:
            _logger.warning("Period should be greater than 0")
        else:
            if len(array) < period:
                _logger.warning("Period greater than length of input. Unexpected behaviour may occur")
            result = talib.ROC(array, period)
            result = remove_nan(result)
        _logger.debug('ROC output: %s' % result)
    return result
