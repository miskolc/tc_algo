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


class Pattern(Enum):
    two_crows = "CDL2CROWS"
    three_black_crows = "CDL3BLACKCROWS"
    three_advancing_black_soldiers = "CDL3WHITESOLDIERS"
    closing_marubozu = "CDLCLOSINGMARUBOZU"
    dark_cloud_cover = "CDLDARKCLOUDCOVER"
    doji = "CDLDOJI"
    doji_star = "CDLDOJISTAR"
    dragonfly_doji = "CDLDRAGONFLYDOJI"
    engulfing_pattern = "CDLENGULFING"
    evening_star = "CDLEVENINGSTAR"
    gravestone_doji = "CDLGRAVESTONEDOJI"
    hammer = "CDLHAMMER"
    hanging_man = "CDLHANGINGMAN"
    harami_pattern = "CDLHARAMI"
    harami_cross_pattern = "CDLHARAMICROSS"
    inverted_hammer = "CDLINVERTEDHAMMER"
    marubozu = "CDLMARUBOZU"
    morning_doji_star = "CDLMORNINGDOJISTAR"
    morning_star = "CDLMORNINGSTAR"
    shooting_star = "CDLSHOOTINGSTAR"
    spinning_top = "CDLSPINNINGTOP"
    tasuki_gap = "CDLTASUKIGAP"
    upside_gap_two_crows = "CDLUPSIDEGAP2CROWS"

    def __str__(self):
        return self.value


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
    return (data is None) | (data == []) | (type(data[0]) != DataObject)


def _get_list(array: numpy.ndarray):
    """
    Converts numpy.ndarray to list
    :param array: numpy.ndarray
    :return: list
    """
    return array.tolist()


def pattern_hunter(data: list, pattern: Pattern):
    """
    Returns a list which defines where pattern is either bullish, bearish or nothing.
    If value in list is between 1 and 100 - bullish
    If value in list is between -1 and -100 - bearish
    If value in list is 0 - Nothing
    :param data: list[DataObject]
    :param pattern: str: Pattern enum
    :return: list[numeric]
    """
    result, pattern_at = [], []
    pattern_info(pattern.value)
    if _check_data(data):
        _logger.warning("Invalid Input for pattern_hunter")
    else:
        open, high, low, close = data_parser.get_ohlc(data)
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
