import logging

import talib
from talib.abstract import Function

import data_parser
from model import *

_logger = logging.getLogger("pattern_hunter")
"""
List of Indicators under pattern_hunter are:
1.	Two Crows
2.	Three Black Crows
3.	Three Advancing White Soldiers
4.	Closing Marubozu
5.	Dark Cloud Cover
6.	Doji
7.	Doji star
8.	Dragonfly doji
9.	Engulfing pattern
10.	Evening star
11.	Gravestone doji
12.	Hammer
13.	Hanging man
14.	Harami pattern 
15.	Harami cross pattern
16.	Inverted hammer
17.	Marubozu
18.	Morning doji star
19.	Morning star
20.	Shooting star
21.	Spinning top
22.	Tasuki gap
23.	Upside gap two crows
"""

"""
These patterns are defined for bullish views:
1.	Three Advancing White Soldiers
2.	Doji
3.	Dragonfly Doji (Not sure of Bullish must be used with trend)
4.	Gravestone Doji (Not sure of Bullish must be used with trend)
5.	Hammer
6.	Inverted Hammer
7.	Morning Doji Star
8.	Morning Star

These patterns are defined for bearish views:
1.	Two Crows
2.	Three black Crows
3.	Dark Cloud Cover
4.	Doji Star
5.	Evening Star
6.	Hanging Man
7.	Shooting Star
8.	Upside Gap Two Crows

These patterns are defined for both bullish and bearish views:
1.	Closing Marubozu
2.	Engulfing Pattern
3.	Harami Pattern
4.	Harami Cross Pattern
5.	Marubozu
6.	Spinning Top
7.	Tasuki Gap

"""


def pattern_info(pattern: Pattern):
    """
    Displays info about the pattern mentioned.
    :param pattern: Any pattern from Pattern
    :return: None
    """
    if pattern is "":
        _logger.warning('Enter valid indicator name. For e.g. pattern_info("CDLMARUBOZU")')
        _logger.info("For complete list visit http://mrjbq7.github.io/ta-lib/funcs.html")
    else:
        _logger.info(Function(pattern).info)


def _check_data(data):
    """
    Check whether data entered is valid.
    :param data: list
    :return: False if data is not list[DataObject]
    """
    return (data is None) | (data == []) | (type(data) != numpy.ndarray)


def _get_list(array: numpy.ndarray):
    """
    Converts numpy.ndarray to list
    :param array: numpy.ndarray
    :return: list
    """
    return array.tolist()


def pattern_hunter(open: list, high: list, low: list, close: list, pattern: Pattern) -> list:
    """
    Returns a list which defines where pattern is either bullish, bearish or nothing.
    If value in list is between 1 and 100 - bullish
    If value in list is between -1 and -100 - bearish
    If value in list is 0 - Nothing
    :param close: list[numeric]
    :param low: list[numeric]
    :param high: list[numeric]
    :param open: list[numeric]
    :param pattern: str: Pattern enum
    :return: list[numeric]
    """
    result, pattern_at = [], []
    pattern_info(pattern.value)
    if (_check_data(open)) & (_check_data(high)) & (_check_data(low)) & (_check_data(close)):
        _logger.warning("Invalid Input for pattern_hunter")
    elif (len(open) != len(high)) | (len(open) != len(low)) | (len(open) != len(close)):
        _logger.warning("Variable data length in pattern hunter")
    else:
        exp = "talib.%s(open, high, low, close)" % pattern
        values = dict(open=open, high=high, low=low, close=close, talib=talib)
        result = eval(exp, values)
        pattern_at = result.nonzero()
        _logger.debug("pattern_hunter recognised %s at these positions: %s" % (pattern.name, pattern_at[0]))
        result = _get_list(result)
    _logger.debug('%s output: %s' % (pattern.name, result))
    return result


def analyse_pattern(array: list):
    """
    Analyses the list whether pattern has a value for bullish, bearish or nothing.
    :param array: list
            list got from pattern_hunter
    :return: None
    """
    if (array is None) | (array == []):
        _logger.warning("Invalid data")
    else:
        for i in array:
            if -100 <= i <= -1:
                _logger.debug("Bearish")
            elif 1 <= i <= 100:
                _logger.debug("Bullish")
            elif i == 0:
                # _logger.debug("Nothing")
                pass
            else:
                _logger.debug("False")
