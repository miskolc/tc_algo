import logging
import numpy
import quandl
from talib import MA_Type

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
    var = data_parser.get_data(start_date="01/01/2018")
    # indicators.indicator_info("STOCH")
    # indicators.rsi(close)
    # indicators.stoch(high, low, close)
    # indicators.sma(close, 25)
    # indicators.ema(close, 20)
    # indicators.macd(close)
    # indicators.bollinger_bands(close)
    # indicators.pivot(date=var['date'], high=var['high'], low=var["low"], close=var['close'])
    # data_parser.timestamp_utc("1533203511")
    date = data_parser.get_date(data=var)
    x = data_parser.date_format(date)
