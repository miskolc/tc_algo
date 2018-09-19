import logging
import definitions
from model import *
from contracts import NSECM, NSECD, NSEFO, BSECD, MCX

from mega_trader import client

# TODO: Following are under development order:
# TODO: 1. Live Broadcast
# TODO: 2. Add command line interface


if __name__ == '__main__':
    logging.basicConfig(level=ct.log_level)
    # scrips.generate_contracts()
    scrips = [NSECM._HDFCAMC_4244, NSECM._INFY_1594, NSECM._ITC_1660]
    client.client_logon("TC", "MTM", "TC", scrips=scrips)
