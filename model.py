import numpy
import data_parser


class DataObject:
    def __init__(self, item=numpy.record):
        self.date = data_parser.date_format([item[0]])[0]
        self.open = item[1]
        self.high = item[2]
        self.low = item[3]
        self.close = item[4]
        self.volume = item[5]
        self.turnover = item[6]

    def __str__(self) -> str:
        return "Date: %s \nOpen: %s \nHigh: %s \nLow: %s \nClose: %s \nVolume: %s \nTurnOver: %s" % (
            self.date, self.open, self.high, self.low, self.close, self.volume, self.turnover)


# class DataObject:
#     def __init__(self, date, open, high, low, close, volume, turnover):
#         self.date = date
#         self.open = open
#         self.high = high
#         self.low = low
#         self.close = close
#         self.volume = volume
#         self.turnover = turnover


class PivotObject:
    def __init__(self, pp, r1, r2, r3, s1, s2, s3):
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
