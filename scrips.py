import xml.etree.ElementTree as ET
from datetime import datetime

import pytz

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


def create_contract_file(contract: str, filename: str):
    tree = ET.parse(contract)
    root = tree.getroot()

    symbol, exchange, gateway, token, instrument, desc, lot, isin, series, strike = [], [], [], [], [], [], [], [], [], []

    for child in root:
        symbol.append(child.findtext(SYMBOL))
        exchange.append(child.findtext(EXCHANGE))
        gateway.append(child.findtext(GATEWAY))
        token.append(child.findtext(TOKEN))
        instrument.append(child.findtext(INSTRUMENT))
        desc.append(child.findtext(DESC))
        lot.append(child.findtext(LOT))
        isin.append(child.findtext(ISIN))
        series.append(child.findtext(SERIES))
        strike.append(child.findtext(STRIKE))

    if filename.__contains__(".py"):
        pass
    else:
        filename = filename + ".py"

    filename = "./contracts/" + filename
    f = open(filename, "w", )
    f.write("""
    \n\"\"\"
    \nThis file was generated on %s IST
    \n\"\"\"
    """ % (datetime.now(tz=pytz.timezone('Asia/Kolkata'))))
    f.write("\nfrom model import Scrip \n\n")
    for i in range(len(symbol)):
        if symbol[i] is not None:
            if symbol[i].__contains__("&"):
                symbol[i] = symbol[i].replace("&", "_and")
            if symbol[i].__contains__("-"):
                symbol[i] = symbol[i].replace("-", "_")
            f.write(
                "_%s_%s = Scrip(symbol=\"%s\", exchange=\"%s\", gateway_id=%d, token_no=%d, instrument=\"%s\", symbol_desc=\"%s\", lot_size=%d, isin_number=\"%s\", series=\"%s\", strike_price=%.2d)\n"
                % (symbol[i], token[i], symbol[i], exchange[i], int(gateway[i]), int(token[i]), instrument[i], desc[i],
                   int(lot[i]), isin[i], series[i], float(strike[i])))
    f.close()


contracts = ["C:/Users/sb/Downloads/Contract/NSECM.xml",
             "C:/Users/sb/Downloads/Contract/NSEFO.xml",
             "C:/Users/sb/Downloads/Contract/NSECD.xml",
             "C:/Users/sb/Downloads/Contract/BSECD.xml",
             "C:/Users/sb/Downloads/Contract/MCX.xml"]
filenames = ["NSECM", "NSEFO", "NSECD", "BSECD", "MCX"]

for i in range(len(contracts)):
    create_contract_file(contracts[i], filenames[i])
