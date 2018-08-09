import logging

import indicators
import data_parser

# TODO: Follow the below order:
# TODO: 1. Make all Indicators - Done
# TODO: 2. Work on OHLC data - Done
# TODO: 3. Build Strategies


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # close = numpy.random.random(105) * 20
    # high = numpy.random.random(105) * 20
    # low = numpy.random.random(105) * 20
    var = data_parser.get_data(start_date="01/12/2008")
    # logging.debug(var)
    # date = data_parser.get_date(var)
    # open = data_parser.get_open(var)
    high = data_parser.get_high(var)
    low = data_parser.get_low(var)
    close = data_parser.get_close(var)
    # indicators.indicator_info("STOCH")
    rsi = indicators.rsi(close)
    stoch = indicators.stoch(high, low, close)
    sma50 = indicators.sma(close, 50)
    sma200 = indicators.sma(close, 200)
    ema = indicators.ema(close, 20)
    macd = indicators.macd(close)
    bbands = indicators.bollinger_bands(close)
    pivot = indicators.pivot(var)
    data_with_indicators = data_parser.data_builder(var, rsi=rsi, stoch=stoch, sma=sma50, sma1=sma200, ema=ema,
                                                    macd=macd, bbands=bbands, pivot=pivot)
    logging.info(data_with_indicators)
    # data_parser.timestamp_utc("1533203511")
    # data = data_parser.get_date_ohlc(start_date="01/01/2018")
    # logging.debug(data)
    # charting.get_candlestick_chart(data)
    # sma50 = indicators.sma(close, period=50)
    # logging.debug(type(sma50))
    # sma200 = indicators.sma(close, period=200)
    # logging.debug(type(sma200))
    # strategy.ma(close, sma1=sma50, sma2=sma200)
