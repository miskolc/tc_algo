import logging
import numpy
import quandl
from talib import MA_Type

import charting
import indicators
import data_parser

# TODO: Follow the below order:
# TODO: 1. Make all Indicators
# TODO: 2. Work on OHLC data
# TODO: 3. Build Strategies

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # close = numpy.random.random(105) * 20
    # high = numpy.random.random(105) * 20
    # low = numpy.random.random(105) * 20
    # var = data_parser.get_data(start_date="01/01/2018")
    # date = data_parser.get_date(var)
    # open = data_parser.get_open(var)
    # high = data_parser.get_high(var)
    # low = data_parser.get_low(var)
    # close = data_parser.get_close(var)
    # indicators.indicator_info("STOCH")
    # indicators.rsi(close)
    # indicators.stoch(high, low, close)
    # indicators.sma(close, 25)
    # indicators.ema(close, 20)
    # indicators.macd(close)
    # indicators.bollinger_bands(close)
    # indicators.pivot(date=var['date'], high=var['high'], low=var["low"], close=var['close'])
    # data_parser.timestamp_utc("1533203511")
    # data = data_parser.get_date_ohlc(start_date="01/01/2018")
    # logging.debug(data)
    # charting.get_candlestick_chart(data)
    data = data_parser.get_data(start_date="01/01/2018")
    logging.debug(data)
    pivots = indicators.pivot(data)
    print(pivots[0][0].date)
    print(pivots[0][1])
    print(pivots[-1][0].date)
    print(pivots[-1][1])
    # for i in range(len(pivots['date'])):
    #     print(pivots['date'][i])
    #     print(pivots['pivot'][i])
