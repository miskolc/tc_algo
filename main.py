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
# TODO: 3. Build Strategies - Done
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
    prop, data = data_parser.get_data(start_date="2017-08-18")
    result = Strategies.ma(data, data_properties=prop)
    print(result['data_properties'])
    print(result['params'])
    print(result['data'])
