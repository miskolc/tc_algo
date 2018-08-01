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
