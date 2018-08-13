import logging
from argparse import ArgumentParser
from datetime import *
import api
import charting
import indicators
import data_parser
from model import Condition, Operation

# TODO: Follow the below order:
# TODO: 1. Make all Indicators - Done
# TODO: 2. Work on OHLC data - Done
# TODO: 3. Build Strategies
# TODO: 4. Add command line interface
import strategy

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # parser = ArgumentParser(description='Trading Campus Python for Finance.')
    # parser.add_argument('-s', '--symbol', '--scrip', metavar=api.nifty50, type=str,
    #                     default=api.nifty50, help='Add a scrip for analysis')
    # parser.add_argument('-sd', '--start-date', dest='start_date', default=api.start_date,
    #                     type=date, help='Start date for the symbol or scrip')
    # parser.add_argument('-ed', '--end-date', dest='end_date', type=date,
    #                     help='Start date for the symbol or scrip')
    # parser.add_argument('--sma', dest="sma",
    #                     help="Finds Simple Moving Average for the given parameters. For e.g. sma_50")
    # parser.add_argument('--ema', dest="ema",
    #                     help="Finds Exponential Moving Average for the given parameters. For e.g. ema_50")
    # parser.add_argument('--rsi', dest="rsi",
    #                     help="Finds Relative Strength Index for the given parameters. For e.g. rsi_50")
    # parser.add_argument('--stoch', dest="stoch",
    #                     help="Finds Stochastic Oscillator for the given parameters."
    #                          "For e.g. stoch_kPeriod_dPeriod_MaType")
    # args = parser.parse_args()
    # print(args.accumulate(args))
    # print(args.accumulate(args.integers))
    # close = numpy.random.random(105) * 20
    # high = numpy.random.random(105) * 20
    # low = numpy.random.random(105) * 20
    var = data_parser.get_data(start_date="01/12/2008")
    # logging.debug(var)
    # date = data_parser.get_date(var)
    # open = data_parser.get_open(var)
    # high = data_parser.get_high(var)
    # low = data_parser.get_low(var)
    close = data_parser.get_close(var)
    # indicators.indicator_info("STOCH")
    # rsi = indicators.rsi(close)
    # stoch = indicators.stoch(high, low, close)
    # sma = indicators.sma(close, 30)
    # ema = indicators.ema(close, 20)
    # macd = indicators.macd(close)
    # bbands = indicators.bollinger_bands(close)
    # pivot = indicators.pivot(var)
    # data_with_indicators = data_parser.data_builder(var, rsi=rsi, stoch=stoch, sma=sma50, sma1=sma200, ema=ema,
    #                                                 macd=macd, bbands=bbands, pivot=pivot)
    # logging.info(data_with_indicators)
    # data_parser.timestamp_utc("1533203511")
    # data = data_parser.get_date_ohlc(start_date="01/01/2018")
    # logging.debug(data)
    rsi = indicators.rsi(close)
    condition1 = Condition(data1=rsi, data2=80, operation=Operation.RANGE_EQUAL)
    result_cond1 = strategy.condition_evaluator(condition=condition1)
    print(result_cond1)
    sma50 = indicators.sma(close, 50)
    sma200 = indicators.sma(close, 200)
    condition2 = Condition(data1=sma50, data2=sma200, operation=Operation.CROSSOVER)
    result_cond2 = strategy.condition_evaluator(condition=condition2)
    print(result_cond2)
    # charting.get_candlestick_chart(data)
    # data = data_parser.get_date_ohlc()
    # charting.get_candlestick_chart(data)
