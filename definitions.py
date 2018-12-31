import logging
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONTRACTS = os.path.join(ROOT_DIR, 'contracts/')
REPORTS = os.path.join(ROOT_DIR, 'reports/')
SPEC = os.path.join(ROOT_DIR, "spec/")
LOG = os.path.join(ROOT_DIR, 'log/')

security = "security"
contract = "contract"
ext = ".txt"
nsecm = security + ext
nsefo = contract + ext
CONTRACT_NSECM = os.path.join(CONTRACTS, nsecm)
CONTRACT_NSEFO = os.path.join(CONTRACTS, nsefo)

BROADCAST_LOG = os.path.join(LOG, 'broadcast.log')
MESSAGE_LOG = os.path.join(LOG, 'messages.log')
MSG_LOG = os.path.join(LOG, 'msg.log')
FIX50SP02 = os.path.join(SPEC + "FIX50SP2.xml")

MEGA_TRADER = os.path.join(ROOT_DIR, "mega_trader/")

MEGA_TRADER_LOG = os.path.join(MEGA_TRADER, "log")
CLIENT_CONFIG = os.path.join(MEGA_TRADER, 'client.cfg')

ALGO = os.path.join(ROOT_DIR, "algo/")
ALGO_CONFIG = os.path.join(ALGO, "config.xml")

directories = [LOG, CONTRACTS, REPORTS, MEGA_TRADER_LOG]

for directory in directories:
    if not os.path.exists(directory):
        try:
            logging.debug("Creating directory: %s" % directory)
            os.makedirs(directory)
            logging.debug("Directory created: %s" % directory)
        except OSError as e:
            print(e)
