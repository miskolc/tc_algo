import logging

# TODO: Following are under development order:
# TODO: 1. Live Broadcast
# TODO: 2. Add command line interface
from contracts import NSECM, NSECD, NSEFO, BSECD, MCX
import scrips
from mega_trader import client

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # scrips.generate_contracts()
    scrips = NSECM.all_scrips
    # print(len(scrips))
    client.client_logon("TC", "MTM", "TC", scrips=scrips)
