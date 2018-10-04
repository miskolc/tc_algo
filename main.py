import logging

import charting
import data_parser
import definitions
import indicators
import strategy
from model import *
from contracts import NSECM, NSECD, NSEFO, BSECD, MCX

from mega_trader import client
import scrips

# TODO: Following are under development order:
# TODO: 1. Options Module
# TODO: 2. Add command line interface


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # scrips.generate_contracts()
    # fo_scrips = scrips.get_fo_scrip_tokens()
    # scrips = fo_scrips + [NSECM._HDFCAMC_4244]
    # client.client_logon("TC", "MTM", "TC", scrips=scrips)
    # # parser = ArgumentParser(description='Trading Campus Python for Finance.')
    # # parser.add_argument('-s', '--symbol', '--scrip', metavar=api.nifty50, type=str,
    # #                     default=api.nifty50, help='Add a scrip for analysis')
    # # parser.add_argument('-sd', '--start-date', dest='start_date', default=api.start_date,
    # #                     type=date, help='Start date for the symbol or scrip')
    # # parser.add_argument('-ed', '--end-date', dest='end_date', type=date,
    # #                     help='Start date for the symbol or scrip')
    # # parser.add_argument('--sma', dest="sma",
    # #                     help="Finds Simple Moving Average for the given parameters. For e.g. sma_50")
    # # parser.add_argument('--ema', dest="ema",
    # #                     help="Finds Exponential Moving Average for the given parameters. For e.g. ema_50")
    # # parser.add_argument('--rsi', dest="rsi",
    # #                     help="Finds Relative Strength Index for the given parameters. For e.g. rsi_50")
    # # parser.add_argument('--stoch', dest="stoch",
    # #                     help="Finds Stochastic Oscillator for the given parameters."
    # #                          "For e.g. stoch_kPeriod_dPeriod_MaType")
    # # args = parser.parse_args()
    # # print(args.accumulate(args))
    # # print(args.accumulate(args.integers))
    data_prop, data = data_parser.get_data(start_date="2012-03-01", interval=Keys.daily)
    high = data_parser.get_high(data)
    low = data_parser.get_low(data)
    close = data_parser.get_close(data)
    sma = indicators.sma(close)
    ema = indicators.ema(close)
    macd = indicators.macd(close)
    rsi = indicators.rsi(close)
    stoch = indicators.stoch(high, low, close)
    bbands = indicators.bollinger_bands(close)
    pivot = indicators.pivot(data, interval=Keys.monthly)
    pivot1 = indicators.pivot(data, interval=Keys.weekly)
    pivot2 = indicators.pivot(data, interval=Keys.daily)
    chart_sma = ChartElement(data=sma, label="sma", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS)
    chart_ema = ChartElement(data=ema, label="ema", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS)
    chart_stoch = ChartElement(data=stoch, label="stoch", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS)
    chart_bbands = ChartElement(data=bbands, label="bbands", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS)
    chart_pivot_month = ChartElement(data=pivot, label="monthly_pivot", chart_type=ChartType.JUMPLINE,
                                     plot=ChartAxis.SAME_AXIS)
    chart_rsi = ChartElement(data=rsi, label="rsi", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS)
    chart_macd = ChartElement(data=macd, label="macd", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS)
    chart_pivot_week = ChartElement(data=pivot1, label="weekly_pivot", chart_type=ChartType.JUMPLINE,
                                    plot=ChartAxis.SAME_AXIS)
    chart_pivot_daily = ChartElement(data=pivot2, label="daily_pivot", chart_type=ChartType.JUMPLINE,
                                     plot=ChartAxis.SAME_AXIS)
    charts = [chart_bbands, chart_macd]
    # charts = [chart_5]
    # buy = Condition(data1=sma, data2=ema, operation=Operation.CROSSOVER)
    # buy1 = Condition(data1=[Pattern.closing_marubozu], data2=[-100, -50], operation=Operation.BEAR_RANGE)
    # sell = Condition(data1=rsi, data2=70, operation=Operation.GREATER_THAN)
    # result = strategy.strategy_builder(data_properties=data_prop, data_list=data, charts=charts, buy=[buy],
    #                                    sell=sell, target=1.0, sl=0.5, strategy=strategy.BUY,
    #                                    backtest_chart=ChartType.COLUMN)
    buy1 = Condition(data1=ema, data2=sma, operation=Operation.CROSSOVER)
    buy2 = Condition(data1=[Pattern.closing_marubozu], data2=[50, 100])
    buy = ConditionsLogic(condition1=buy1, condition2=buy2, logical=Logical.OR)
    sell = Condition(data1=ema, data2=sma, operation=Operation.CROSSUNDER)
    sell_1 = Condition(data1=[Pattern.doji_star], operation=Operation.BEAR_RANGE)

    result = strategy.strategy_builder(data_properties=data_prop, data_list=data, charts=charts, buy=buy1,
                                       sell=[sell, sell_1], target=1.8, sl=0.7, strategy=strategy.BUY,
                                       backtest_chart=ChartType.COLUMN, )
    # strategy.strategy_optimizations(data_properties=data_prop, data_list=data, buy=[buy, buy1],
    #                                 sell=sell, target_range=[1.0, 1.3, 1.9, 2.2],
    #                                 sl_range=[0.3, 0.5, 0.6, 0.8], strategy=strategy.BUY, )
    # strategy.strategy_optimizations(data_properties=data_prop, data_list=data, buy=[buy, buy1],
    #                                 sell=sell, target_range=numpy.arange(0.3, 1.8, 0.2),
    #                                 sl_range=numpy.arange(0.1, 0.9, 0.1), strategy=strategy.BUY,)
    # strategy.strategy_optimizations(data_properties=data_prop, data_list=data, buy=[buy, buy1],
    #                                 sell=sell, target_range=numpy.arange(0.3, 1.8, 0.2),
    #                                 sl_range=0.3, strategy=strategy.BUY, )

    # data_prop, data = data_parser.get_data(start_date="2012-03-01", interval=Keys.daily)
    # patterns = [Pattern.harami_pattern, Pattern.spinning_top, Pattern.tasuki_gap]
    # data_prop, params, data_list, pattern_data = data_parser.data_builder(data, data_prop, )
    # result = {
    #     Keys.data_prop: data_prop,
    #     Keys.data: data_list,
    #     Keys.params: params,
    #     Keys.patterns: pattern_data,
    # }
    app = charting.create_app(result)
    app.run()
    # strategy.Strategies.macd(data, data_prop)
    # # strategy.show_back_testing_reports(result)
    # # result = pattern_hunter.pattern_hunter(data, pattern=Pattern.doji)
    # # pattern_hunter.analyse_pattern(result)
    #
