from typing import Union
from decimal import *
from dateutil import parser
from enum import Enum

import numpy

import constants as ct
from constants import Keys

PRECISION = Decimal(10) ** -2


class Symbol:

    def __init__(self, scrip: str, api_key: str, size: int):
        self.scrip = scrip
        self.api_key = api_key
        self.size = size


class DataObject:
    """
    A class for creating an object which contains candle data.
    """

    def __init__(self, item: numpy.record):
        """
        Converts data received from Quandl in DataObject
        :param item: numpy.record
                Received from Quandl API
        """
        self.date = date_format([item[0]])[0]
        self.open = item[1]
        self.high = item[2]
        self.low = item[3]
        self.close = item[4]
        self.volume = item[5]
        self.turnover = item[6]

    def __str__(self) -> str:
        return "Date: %s \nOpen: %s \nHigh: %s \nLow: %s \nClose: %s \nVolume: %s \nTurnOver: %s" % (
            self.date, self.open, self.high, self.low, self.close, self.volume, self.turnover)


class PivotObject:
    """
    A class for creating an object which contains pivot related data
    """

    def __init__(self, pp=ct.default, r1=ct.default, r2=ct.default, r3=ct.default,
                 s1=ct.default, s2=ct.default, s3=ct.default):
        """
        Pivot data
        :param pp: Pivot Point
        :param r1: Resistance level 1
        :param r2: Resistance level 2
        :param r3: Resistance level 3
        :param s1: Support level 1
        :param s2: Support level 2
        :param s3: Support level 3
        """
        self.pp = pp
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def __str__(self) -> str:
        return "Pivot values are: \nPP = %s \nR1 = %s \nS1 = %s \nR2 = %s \nS2 = %s \nR3 = %s \nS3 = %s" % (
            self.pp, self.r1, self.s1, self.r2, self.s2, self.r3, self.s3)


def date_format(date_array=None):
    """
    This only required for quandl data where date is in ISO format
    :param date_array: list where date is in ISO format
    :return: list of date in datetime.date object
    """
    result = []
    if date_array is None:
        date_array = []
    x = numpy.datetime_as_string(date_array)
    for i in x:
        i = parser.parse(i).date()
        result.append(i)
    return result


class Operation(Enum):
    """
    This class is used to define operation for data in a Condition Object
    """
    EQUAL = "="
    GREATER_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    CROSSOVER = "CROSSOVER"
    CROSSUNDER = "CROSSUNDER"
    RANGE_EQUAL = "<=  <="

    def __str__(self):
        return self.value


class Condition:
    """
    This class is used to define condition between two data list.
    """
    data1 = None
    data2 = None
    operation = None

    def __init__(self, data1=list, data2=list, operation=Operation):
        """
        Initialize a Condition which can be between any list & list or list & constant.
        list should contain numeric values or default or None values.
        For e.g. Condition(data1 = indicator1, data2= indicator2, operation= Operation.EQUAL)
        :param data1: list
        :param data2: list or numeric
        :param operation: Operation
        """
        self.data1 = data1
        self.data2 = data2
        self.operation = operation

    def __str__(self) -> str:
        return "data1 %s data2" % self.operation


class Logical(Enum):
    """
    This class is used to define logical operation between two Condition Objects
    in ConditionLogic object
    """
    AND = "&"
    OR = "|"

    def __str__(self):
        return self.value


class ConditionsLogic:
    """
    This class is used to define condition between two Condition Objects.
    This ConditionLogic can only be used between two Condition Objects.
    """
    logic = None
    cond1 = None
    cond2 = None

    def __init__(self, condition1=Condition, condition2=Condition, logical=Logical):
        """
        It initializes a ConditionLogic object.
        :param condition1: Condition
        :param condition2: Condition
        :param logical: Logical
        """
        self.cond1 = condition1
        self.cond2 = condition2
        self.logic = logical


class ChartType(Enum):
    """
    This class defines the type of chart in ChartElement object
    """
    CANDLESTICK = "candlestick"
    LINE = 'line'
    COLUMN = 'column'

    def __str__(self):
        return self.value


class ChartAxis(Enum):
    """
    This class defines the chart axis in ChartElement object
    """
    SAME_AXIS = 0
    DIFFERENT_AXIS = 1

    def __str__(self):
        return str(self.value)


class ChartColor(Enum):
    """
    This class defines the color of element in ChartElement object
    """
    RED = 'RED'
    BLUE = 'BLUE'
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    PINK = 'PINK'
    PURPLE = 'PURPLE'

    def __str__(self):
        return self.value


class ChartElement:
    """
    This class is used to define a Charting element which needs to be plotted on the chart
    """
    def __init__(self, data: Union[list, dict], label: str, chart_type: ChartType, plot: Union[int, ChartAxis],
                 color: Union[ChartColor, str]):
        """
        It initializes a ChartElement to be plotted on chart either through strategy or data_builder
        :param data: Union[list, dict]
        :param label: str
                Name of the element on the chart
        :param chart_type: ChartType
                    Type of chart
        :param plot: Union[int, ChartAxis]
                    Axis of chart element. It can be an Integer or ChartAxis enum.
        :param color: Union[ChartColor, str]
                    Color of chart element. It can be an str or ChartColor enum.
        """
        self.data = data
        self.type = chart_type
        self.axis = plot
        self.color = color
        self.label = label


class Pattern(Enum):
    """
    Pattern Keys for pattern hunter
    """
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
