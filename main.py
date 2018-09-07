import logging
from argparse import ArgumentParser
from datetime import *

import quickfix

import api
import charting
import indicators
import data_parser
import pattern_hunter
from mega_trader.client import ClientApplication
from pattern_hunter import Pattern
from model import *
import strategy
from strategy import Strategies

# TODO: Following are under development order:
# TODO: 1. Add command line interface


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    filename = "mega_trader/client.cfg"
    try:
        settings = quickfix.SessionSettings(filename)
        application = ClientApplication
        storeFactory = quickfix.FileStoreFactory(settings)
        logFactory = quickfix.FileLogFactory(settings)
        initiator = quickfix.SocketInitiator(application, storeFactory, settings, logFactory)
        initiator.start()
        # while condition == true: do something
        initiator.stop()
    except quickfix.ConfigError as e:
        print(e)
