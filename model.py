import numpy
from dateutil import parser
from enum import Enum


class DataObject:
    def __init__(self, item=numpy.record):
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
    def __init__(self, pp=None, r1=None, r2=None, r3=None, s1=None, s2=None, s3=None):
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


# This only required for quandl data where date is in ISO format
def date_format(date_array=None):
    result = []
    if date_array is None:
        date_array = []
    x = numpy.datetime_as_string(date_array)
    for i in x:
        i = parser.parse(i).date()
        result.append(i)
    return result


class Operation(Enum):
    EQUAL = "="
    GREATER_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="
    GREATER = ">"
    LESS = "<"
    CROSSOVER = "CROSSOVER"
    CROSSUNDER = "CROSSUNDER"
    RANGE_EQUAL = "<=  <="

    def __str__(self):
        return self.value


class Condition:
    data1 = None
    data2 = None
    operation = None

    def __init__(self, data1=list, data2=list, operation=Operation):
        self.data1 = data1
        self.data2 = data2
        self.operation = operation

    def __str__(self) -> str:
        return "data1 %s data2" % self.operation


class Logical(Enum):
    AND = "&"
    OR = "|"

    def __str__(self):
        return self.value


class ConditionsLogic:
    def __init__(self, condition1=Condition, condition2=Condition, logical=Logical):
        self.cond1 = condition1
        self.cond2 = condition2
        self.logic = logical
