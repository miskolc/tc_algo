import os
import xml.etree.ElementTree as ET
from datetime import datetime

import pytz
import logging

_logger = logging.getLogger("contract_manager")

SYMBOL = "Symbol"
EXCHANGE = "Exchange"
GATEWAY = "GatewayId"
TOKEN = "TokenNo"
INSTRUMENT = "InstrumentName"
DESC = "SymbolDesc"
LOT = "LotSize"
ISIN = "ISINNumber"
SERIES = "Series"
STRIKE = "StrikePrice"


def create_contract_file(contract: str, filename: str, path: str = None):
    tree = ET.parse(contract)
    root = tree.getroot()

    symbol, exchange, gateway, token, instrument, desc, lot, isin, series, strike = [], [], [], [], [], [], [], [], [], []

    _logger.debug("Reading contract file")
    for child in root:
        symb = child.findtext(SYMBOL)
        if symb is not None:
            symbol.append(child.findtext(SYMBOL))
            exchange.append(child.findtext(EXCHANGE))
            gateway.append(int(child.findtext(GATEWAY)))
            token.append(int(child.findtext(TOKEN)))
            instrument.append(child.findtext(INSTRUMENT))
            desc.append(child.findtext(DESC))
            lot.append(int(child.findtext(LOT)))
            isin.append(child.findtext(ISIN))
            series.append(child.findtext(SERIES))
            strike.append(float(child.findtext(STRIKE)))
    _logger.debug("Reading contract file complete")

    if path is None:
        path = "./contracts/"
    init = "__init__.py"
    init_file = path + init

    if not os.path.exists(path):
        try:
            _logger.debug("Creating path %s" % path)
            os.makedirs(path)
            _logger.debug("Path created")
        except OSError as e:
            print(e)
    if not os.path.exists(init_file):
        _logger.debug("Creating file %s" % init_file)
        f = open(init_file, "w")
        f.write("# Don't delete this file.\n")
        f.close()
        _logger.debug("File created")

    if filename.__contains__(".py"):
        pass
    else:
        filename = filename + ".py"

    filename = path + filename
    f = open(filename, "w", )
    f.write("""
    \n\"\"\"
    \nThis file was generated on %s IST
    \n\"\"\"
    """ % (datetime.now(tz=pytz.timezone('Asia/Kolkata'))))
    f.write("\nfrom model import Scrip \n\n")

    all_scrips = "all_scrips = ["
    for i in range(len(symbol)):
        if symbol[i].__contains__(" "):
            symbol[i] = symbol[i].replace(" ", "_")
        if symbol[i].__contains__("."):
            symbol[i] = symbol[i].replace(".", "_")
        if symbol[i].__contains__("&"):
            symbol[i] = symbol[i].replace("&", "_and")
        if symbol[i].__contains__("-"):
            symbol[i] = symbol[i].replace("-", "_")

        if strike[i] == "-01":
            print(symbol[i])
            strike[i] = "-1"
        name = "_%s_%s" % (symbol[i], token[i])
        all_scrips += "%s, " % name
        f.write(
            "%s = Scrip(symbol=\"%s\", exchange=\"%s\", gateway_id=%d, token_no=%d, instrument=\"%s\", symbol_desc=\"%s\", lot_size=%d, isin_number=\"%s\", series=\"%s\", strike_price=%.2f)\n"
            % (name, symbol[i], exchange[i], gateway[i], token[i], instrument[i], desc[i],
               lot[i], isin[i], series[i], strike[i]))

    all_scrips += "]"
    _logger.debug(all_scrips)
    f.write("\n")
    f.write(all_scrips)
    f.close()


def generate_contracts(path: str = None):
    contracts = ["C:/Users/sb/Downloads/Contract/NSECM.xml",
                 "C:/Users/sb/Downloads/Contract/NSEFO.xml",
                 "C:/Users/sb/Downloads/Contract/NSECD.xml",
                 "C:/Users/sb/Downloads/Contract/BSECD.xml",
                 "C:/Users/sb/Downloads/Contract/MCX.xml"]
    filenames = ["NSECM", "NSEFO", "NSECD", "BSECD", "MCX"]
    # contracts = ["C:/Users/sb/Downloads/Contract/NSECD.xml"]
    # filenames = ["NSECD"]

    for i in range(len(contracts)):
        create_contract_file(contracts[i], filenames[i], path)
    _logger.info("Contracts generated")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    generate_contracts()
    generate_contracts()
