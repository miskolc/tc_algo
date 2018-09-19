import logging
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT_DIR, 'log/')
BROADCAST_LOG = os.path.join(LOG, 'broadcast.log')
MESSAGE_LOG = os.path.join(LOG, 'messages.log')
MSG_LOG = os.path.join(LOG, 'msg.log')
CONTRACTS = os.path.join(ROOT_DIR, 'contracts/')
REPORTS = os.path.join(ROOT_DIR, 'reports/')

nsecm = "security"
nsefo = "contract"
ext = ".txt"
CONTRACT_NSECM = os.path.join(CONTRACTS, nsecm + ext)
CONTRACT_NSEFO = os.path.join(CONTRACTS, nsefo + ext)

MEGA_TRADER = os.path.join("mega_trader/")
CLIENT_CONFIG = os.path.join(MEGA_TRADER, 'client.cfg')

directory = [LOG, CONTRACTS, REPORTS]

for dir in directory:
    if not os.path.exists(dir):
        try:
            logging.debug("Creating directory: %s" % dir)
            os.makedirs(dir)
            logging.debug("Directory created: %s" % dir)
        except OSError as e:
            print(e)
