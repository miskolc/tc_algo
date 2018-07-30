import logging

import talib
from talib.abstract import Function
import numpy

_logger = logging.getLogger('indicator')


# Get info for the required function in ta-lib
def indicator_info(indicator=str()):
    var = Function(indicator).info
    _logger.info(var)


# Simple moving average. Default period = 30
def remove_nan(result):
    where_are_nan = numpy.isnan(result)
    result[where_are_nan] = 0
    return result


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
