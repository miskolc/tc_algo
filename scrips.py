import os
import xml.etree.ElementTree as ET
from datetime import datetime

import pytz
import logging

import definitions
from model import ct

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

fo = ["ACC", "ADANIENT", "ADANIPORTS", "ADANIPOWER", "AJANTPHARM", "ALBK", "AMARAJABAT", "AMBUJACEM", "ANDHRABANK",
      "APOLLOHOSP", "APOLLOTYRE", "ARVIND", "ASHOKLEY", "ASIANPAINT", "AUROPHARMA", "AXISBANK", "BAJAJ-AUTO",
      "BAJAJFINSV", "BAJFINANCE", "BALKRISIND", "BALRAMCHIN", "BANKBARODA", "BANKINDIA", "BATAINDIA", "BEL", "BEML",
      "BERGEPAINT", "BHARATFIN", "BHARATFORG", "BHARTIARTL", "BHEL", "BIOCON", "BOSCHLTD", "BPCL", "BRITANNIA",
      "CADILAHC", "CANBK", "CANFINHOME", "CAPF", "CASTROLIND", "CEATLTD", "CENTURYTEX", "CESC", "CGPOWER", "CHENNPETRO",
      "CHOLAFIN", "CIPLA", "COALINDIA", "COLPAL", "CONCOR", "CUMMINSIND", "DABUR", "DALMIABHA", "DCBBANK", "DHFL",
      "DISHTV", "DIVISLAB", "DLF", "DRREDDY", "EICHERMOT", "ENGINERSIN", "EQUITAS", "ESCORTS", "EXIDEIND", "FEDERALBNK",
      "GAIL", "GLENMARK", "GMRINFRA", "GODFRYPHLP", "GODREJCP", "GODREJIND", "GRANULES", "GRASIM", "GSFC", "HAVELLS",
      "HCC", "HCLTECH", "HDFC", "HDFCBANK", "HEROMOTOCO", "HEXAWARE", "HINDALCO", "HINDPETRO", "HINDUNILVR", "HINDZINC",
      "IBULHSGFIN", "ICICIBANK", "ICICIPRULI", "IDBI", "IDEA", "IDFC", "IDFCBANK", "IFCI", "IGL", "INDIACEM", "INDIANB",
      "INDIGO", "INDUSINDBK", "INFIBEAM", "INFRATEL", "INFY", "IOC", "IRB", "ITC", "JETAIRWAYS", "JINDALSTEL",
      "JISLJALEQS", "JPASSOCIAT", "JSWSTEEL", "JUBLFOOD", "JUSTDIAL", "KAJARIACER", "KOTAKBANK", "KPIT", "KSCL",
      "KTKBANK", "L&TFH", "LICHSGFIN", "LT", "LUPIN", "M&M", "M&MFIN", "MANAPPURAM", "MARICO", "MARUTI", "MCDOWELL-N",
      "MCX", "MFSL", "MGL", "MINDTREE", "MOTHERSUMI", "MRF", "MRPL", "MUTHOOTFIN", "NATIONALUM", "NBCC", "NCC",
      "NESTLEIND", "NHPC", "NIITTECH", "NMDC", "NTPC", "OFSS", "OIL", "ONGC", "ORIENTBANK", "PAGEIND", "PCJEWELLER",
      "PEL", "PETRONET", "PFC", "PIDILITIND", "PNB", "POWERGRID", "PTC", "PVR", "RAMCOCEM", "RAYMOND", "RBLBANK",
      "RCOM", "RECLTD", "RELCAPITAL", "RELIANCE", "RELINFRA", "REPCOHOME", "RPOWER", "SAIL", "SBIN", "SHREECEM",
      "SIEMENS", "SOUTHBANK", "SREINFRA", "SRF", "SRTRANSFIN", "STAR", "SUNPHARMA", "SUNTV", "SUZLON", "SYNDIBANK",
      "TATACHEM", "TATACOMM", "TATAELXSI", "TATAGLOBAL", "TATAMOTORS", "TATAMTRDVR", "TATAPOWER", "TATASTEEL", "TCS",
      "TECHM", "TITAN", "TORNTPHARM", "TORNTPOWER", "TV18BRDCST", "TVSMOTOR", "UBL", "UJJIVAN", "ULTRACEMCO",
      "UNIONBANK", "UPL", "VEDL", "VGUARD", "VOLTAS", "WIPRO", "WOCKPHARMA", "YESBANK", "ZEEL"]


def get_fo_symbols():
    result = []
    print(len(fo))
    for scrip in fo:
        result.append(rectify_symbol(scrip))
    return result


def get_fo__scrip_tokens():
    from contracts import NSECM
    fo_symbols = get_fo_symbols()
    tokens = []
    for symbol in fo_symbols:
        for scrip in NSECM.all_scrips:
            if scrip.symbol == symbol:
                tokens.append(scrip)

    return tokens


def create_contract_file(contract: str, gateway_id: ct.Gateway, path: str = None):
    symbol, exchange, gateway, token, instrument, desc, lot, isin, series, strike = [], [], [], [], [], [], [], [], [], []

    # Read File according to type
    if contract.__contains__(".xml"):
        # MultiChart XML File
        tree = ET.parse(contract)
        root = tree.getroot()
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
    elif contract.__contains__(".txt"):
        # NEAT from NSE FTP
        f = open(contract, "r")
        lines = f.readlines()
        for line in lines:
            arr = line.split("|")
            if len(arr) == 54:
                # NSECM security
                if str(arr[2]) == "EQ":
                    symbol.append(str(arr[1]))
                    exchange.append(str(gateway_id.name))
                    gateway.append(int(gateway_id.value))
                    token.append(int(arr[0]))
                    instrument.append(str(ct.default))
                    desc.append(str(arr[21]))
                    lot.append(int(arr[19]))
                    isin_part = str(arr[53])
                    isin_part = isin_part.replace("\n", "")
                    isin.append(isin_part)
                    series.append(arr[2])
                    strike.append(float("0"))
            elif len(arr) == 69:
                # NSEFO contract
                symbol.append(str(arr[3]))
                exchange.append(str(gateway_id.name))
                gateway.append(int(gateway_id.value))
                token.append(int(arr[0]))
                instrument.append(str(arr[2]))
                desc.append(str(arr[53]))
                lot.append(int(arr[30]))
                isin.append(str(ct.default))
                series.append(arr[8])
                strike.append(float(arr[7]))
    # Create py file
    if path is None:
        path = definitions.CONTRACTS
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

    gateway_id = gateway_id.name + ".py"
    gateway_id = path + gateway_id
    f = open(gateway_id, "w", )
    f.write("""
    \n\"\"\"
    \nThis file was generated on %s IST
    \n\"\"\"
    """ % (datetime.now(tz=pytz.timezone('Asia/Kolkata'))))
    f.write("\nfrom model import Scrip \n\n")

    token_symbol = "token_symbol = {"
    all_scrips = "all_scrips = ["
    for i in range(len(symbol)):
        symbol[i] = rectify_symbol(symbol[i])
        if strike[i] == "-01":
            print(symbol[i])
            strike[i] = "-1"
        name = "_%s_%s" % (symbol[i], token[i])
        all_scrips += "%s, " % name

        token_symbol_element = "%s: \"%s\", " % (token[i], str(symbol[i] + "^" + desc[i]))
        token_symbol += token_symbol_element
        f.write(
            "%s = Scrip(symbol=\"%s\", exchange=\"%s\", gateway_id=%d, token_no=%d, instrument=\"%s\", symbol_desc=\"%s\", lot_size=%d, isin_number=\"%s\", series=\"%s\", strike_price=%.2f)\n"
            % (name, symbol[i], exchange[i], gateway[i], token[i], instrument[i], desc[i],
               lot[i], isin[i], series[i], strike[i]))

    token_symbol += "}"
    all_scrips += "]"
    _logger.debug(all_scrips)
    f.write("\n%s" % token_symbol)
    f.write("\n%s" % all_scrips)
    # f.write(all_scrips)
    f.close()


def rectify_symbol(symbol):
    if symbol.__contains__(" "):
        symbol = symbol.replace(" ", "_")
    if symbol.__contains__("."):
        symbol = symbol.replace(".", "_")
    if symbol.__contains__("&"):
        symbol = symbol.replace("&", "_and")
    if symbol.__contains__("-"):
        symbol = symbol.replace("-", "_")
    return symbol


def generate_contracts(path: str = None):
    contracts_raw = [definitions.CONTRACT_NSECM,
                     definitions.CONTRACT_NSEFO]
    gateways = [ct.Gateway.NSECM,
                ct.Gateway.NSEFO]

    for i in range(len(contracts_raw)):
        create_contract_file(contracts_raw[i], gateways[i], path)
    _logger.info("Contracts generated")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    generate_contracts()
