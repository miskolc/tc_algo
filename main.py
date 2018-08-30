import logging
from argparse import ArgumentParser
from datetime import *
import api
import charting
import indicators
import data_parser
import pattern_hunter
from pattern_hunter import Pattern
from model import *
import strategy
from strategy import Strategies

# TODO: Following are under development order:
# TODO: 1. Pattern Hunting and its implementation in strategy
# TODO: 2. Weekly, Monthly Data and same for pivots
# TODO: 3. Strategy Optimization
# TODO: 4. Add command line interface


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
    data_prop, data = data_parser.get_data(start_date="2012-08-01", interval=Keys.weekly)
    high = data_parser.get_high(data)
    low = data_parser.get_low(data)
    close = data_parser.get_close(data)
    sma = indicators.sma(close)
    ema = indicators.ema(close)
    macd = indicators.macd(close)
    rsi = indicators.rsi(close)
    stoch = indicators.stoch(high, low, close)
    bbands = indicators.bollinger_bands(close)
    pivot = indicators.pivot(data)
    chart_1 = ChartElement(data=sma, label="sma", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.YELLOW)
    chart_2 = ChartElement(data=ema, label="ema", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.PINK)
    chart_3 = ChartElement(data=stoch, label="stoch", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS,
                           color=ChartColor.PURPLE)
    chart_4 = ChartElement(data=bbands, label="bbands", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.BLUE)
    chart_5 = ChartElement(data=pivot, label="pivot", chart_type=ChartType.JUMPLINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.GREEN)
    chart_6 = ChartElement(data=rsi, label="rsi", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS,
                           color=ChartColor.RED)
    chart_7 = ChartElement(data=macd, label="macd", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS,
                           color="magenta")
    charts = [chart_1, chart_2, chart_3, chart_4, chart_5, chart_6, chart_7]
    buy = Condition(data1=sma, data2=ema, operation=Operation.CROSSOVER)
    buy1 = Condition(data1=Pattern.closing_marubozu, data2=[-100, -50], operation=Operation.BEAR_RANGE)
    sell = Condition(data1=rsi, data2=70, operation=Operation.GREATER_THAN)
    result = strategy.strategy_builder(data_properties=data_prop, data_list=data, charts=charts, buy=[buy, buy1],
                                       sell=sell, target=1.0, sl=0.5, strategy=strategy.BUY, )
    app = charting.create_app(result)
    app.run()
    # strategy.show_back_testing_reports(result)
    # result = pattern_hunter.pattern_hunter(data, pattern=Pattern.doji)
    # pattern_hunter.analyse_pattern(result)
