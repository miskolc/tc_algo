import numpy


class DataObject:
    def __init__(self, item=numpy.record):
        self.date = item[0]
        self.open = item[1]
        self.high = item[2]
        self.low = item[3]
        self.close = item[4]
        self.volume = item[5]
        self.turnover = item[6]


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
    def __init__(self, pp=0, r1=0, r2=0, r3=0, s1=0, s2=0, s3=0):
        self.pp = pp
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def __str__(self) -> str:
        return "PP = %s \n R1 = %s \n S1 = %s \n R2 = %s \n S2 = %s \n R3 = %s \n S3 = %s" % (
            self.pp, self.r1, self.s1, self.r2, self.s2, self.r3, self.s3)
