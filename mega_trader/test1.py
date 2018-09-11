import xml.etree.ElementTree as ET

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

tree = ET.parse('C:/Users/sb/Downloads/Contract/NSECM.xml')
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

f = open("contracts.py", "w", )
f.write("from model import Scrip \n\n")
for i in range(len(symbol)):
    if symbol[i] is not None:
        f.write(
            "_%s_%s = Scrip(symbol='%s', exchange='%s', gateway_id=%d, token_no=%d, instrument='%s', symbol_desc='%s', lot_size=%d, isin_number='%s', series='%s', strike_price=%.2d)\n"
            % (symbol[i], token[i], symbol[i], exchange[i], int(gateway[i]), int(token[i]), instrument[i], desc[i],
               int(lot[i]), isin[i], series[i], float(strike[i])))
f.close()
# child = root[1]
# # for i in child:
# #     print("%s: %s" % (i.tag, i.text))
# symbol = []
# for a in root.iter('Symbol'):
#     symbol.append(a.text)
# print(len(symbol))
#
# exchange = []
# for a in root.iter('Exchange'):
#     exchange.append(a.text)
# print(len(exchange))
#
# gateway_id = []
# for a in root.iter('GatewayId'):
#     gateway_id.append(a.text)
# print(len(gateway_id))
#
# token_no = []
# for a in root.iter('TokenNo'):
#     token_no.append(a.text)
# print(len(token_no))
#
# instrument = []
# for a in root.iter('InstrumentName'):
#     instrument.append(a.text)
# print(len(instrument))
#
# symbol_desc = []
# for a in root.iter('SymbolDesc'):
#     symbol_desc.append(a.text)
# print(len(symbol_desc))
#
# isin_number = []
# for a in root.iter('ISINNumber'):
#     isin_number.append(a.text)
# print(len(isin_number))
