import logging
from argparse import ArgumentParser
from datetime import *
import api
import charting
import indicators
import data_parser
from model import *
import strategy
from strategy import Strategies

# TODO: Follow the below order:
# TODO: 1. Make all Indicators - Done
# TODO: 2. Work on OHLC data - Done
# TODO: 3. Build Strategies
# TODO: 4. Back Testing
# TODO: 5. Add command line interface

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
    var = data_parser.get_data()
    # logging.debug(var)
    # date = data_parser.get_date(var)
    # open = data_parser.get_open(var)
    # high = data_parser.get_high(var)
    # low = data_parser.get_low(var)
    # close = data_parser.get_close(var)
    # indicators.indicator_info("STOCH")
    # rsi = indicators.rsi(close)
    # stoch = indicators.stoch(high, low, close)
    # sma = indicators.sma(close, 30)
    # ema = indicators.ema(close, 30)
    # macd = indicators.macd(close)
    # bbands = indicators.bollinger_bands(close)
    # pivot = indicators.pivot(var)
    # chart1 = ChartElement(data=rsi, chart_type=ChartType.LINE, axis=ChartAxis.DIFFERENT_AXIS, color=ChartColor.RED,
    #                       label="RSI")
    # chart2 = ChartElement(data=stoch, chart_type=ChartType.LINE, axis=ChartAxis.ON_AXIS, color=ChartColor.BLUE,
    #                       label="STOCH")
    # chart3 = ChartElement(data=sma, chart_type=ChartType.LINE, axis=ChartAxis.ON_AXIS, color=ChartColor.PINK,
    #                       label="SMA")
    # chart4 = ChartElement(data=ema, chart_type=ChartType.LINE, axis=ChartAxis.ON_AXIS, color=ChartColor.PURPLE,
    #                       label="EMA")
    # chart5 = ChartElement(data=macd, chart_type=ChartType.LINE, axis=ChartAxis.ON_AXIS, color=ChartColor.YELLOW,
    #                       label="MACD")
    # chart6 = ChartElement(data=bbands, chart_type=ChartType.LINE, axis=ChartAxis.ON_AXIS, color=ChartColor.GREEN,
    #                       label="BBANDS")
    # chart7 = ChartElement(data=pivot, chart_type=ChartType.LINE, axis=ChartAxis.ON_AXIS, color="Magenta",
    #                       label="Pivot")
    # charts = [chart1, chart2, chart3, chart4, chart5, chart6, chart7]
    # data_with_indicators = data_parser.data_builder(var, charts=charts)
    # print(data_with_indicators)
    # logging.info(data_with_indicators)
    # data_parser.timestamp_utc("1533203511")
    # data = data_parser.get_date_ohlc(start_date="01/01/2018")
    # logging.debug(data)
    # ema9 = indicators.ema(close, 9)
    # ema18 = indicators.sma(close, 18)
    # condition1 = Condition(data1=ema9, data2=ema18, operation=Operation.CROSSUNDER)
    # result_cond = strategy._condition_evaluator(condition=condition1)
    # for i in range(len(close)):
    #     if result_cond[i] is True:
    #         print("Date: %s, Close: %s" % (date[i], close[i]))
    # condition1 = Condition(data1=sma, data2=ema, operation=Operation.CROSSOVER)
    # condition2 = Condition(data1=rsi, data2=40, operation=Operation.LESS_THAN)
    # condition3 = Condition(data1=ema9, data2=ema18, operation=Operation.CROSSOVER)
    # condition4 = Condition(data1=sma, data2=ema, operation=Operation.CROSSUNDER)
    # condition5 = Condition(data1=rsi, data2=70, operation=Operation.GREATER_THAN)
    # logic = ConditionsLogic(condition1=condition1, condition2=condition2, logical=Logical.OR)
    # reqd_indicators = dict(rsi=rsi, stoch=stoch, sma=sma, ema=ema, macd=macd, bbands=bbands, pivot=pivot)
    # buy = [logic, condition3]
    # sell = [condition4, condition5]
    # result = strategy.strategy_builder(data_list=var, strategy=strategy.BUY, buy=condition1, sell=condition4,
    #                                    indicator=reqd_indicators, target=condition5, sl=condition2)

    # strategy.show_results(result)
    # Strategies.ma(var, ma_type=1)
    Strategies.rsi(var)
    # Strategies.macd(var)
    # Strategies.stoch(var)
    # Strategies.bbands(var)
    # Strategies.pivot(var)
