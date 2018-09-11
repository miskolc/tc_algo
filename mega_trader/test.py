import socket
import sys

import quickfix as fix
import quickfix50sp2 as fix50
import logging

logging.basicConfig(level=logging.DEBUG, filename="./broadcast.log", filemode="w",
                    format="%(asctime)s:%(message)s")
_logger = logging.getLogger("test")


def test_msg():
    test = fix.Message()
    test.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))


def logon_msg():
    logon_req = fix.Message()
    logon_req.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
    logon_req.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
    logon_req.setField(fix.SenderCompID("AP"))
    logon_req.setField(fix.TargetCompID("MTBM"))
    logon_req.setField(fix.MsgSeqNum(1))
    logon_req.setField(fix.UserRequestType(1))
    logon_req.setField(fix.HeartBtInt(1))
    logon_req.setField(fix.Username("AP"))
    logon_req.setField(fix.NetworkResponseID("14"))
    logon_req.setField(fix.DefaultApplVerID(fix.ApplVerID_FIX50SP2))
    logon_req.setField(1701, "1")
    logon_req.getTrailer().setField(fix.MarketID("2"))
    logon_req.setField(fix.DefaultApplVerID("FIX.5.0SP2"))
    logon_req = bytes(logon_req.toString(), encoding="UTF-8")
    return logon_req


def scrip_msg():
    scrip = fix.Message()
    scrip.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
    scrip.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
    scrip.getHeader().setField(fix.SenderCompID("AP"))
    scrip.getHeader().setField(fix.TargetCompID("MTBM"))
    scrip.setField(fix.MsgSeqNum(1))
    scrip.setField(fix.SenderSubID("NSECM"))
    scrip.setField(fix.UserRequestType(1))
    scrip.setField(115, "1")
    scrip.setField(fix.Symbol("RELIANCE"))
    scrip.setField(1775, "0")
    scrip.setField(167, "")
    scrip.setField(48, "2885")
    scrip.setField(263, "0")
    print(scrip)
    scrip = bytes(scrip.toString(), encoding="UTF-8")
    return scrip


TCP_IP = '192.168.6.107'
TCP_PORT = 2002
BUFFER_SIZE = 1024
address = (TCP_IP, TCP_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

logon = logon_msg()
s.sendto(logon, address)

# token = "8=FIXT.1.1 9=80 35=V 49=MTC 56=MTBM 34=1 50=NSECM 924=1 115=2 48=10580 1775=0 263=0 55=TCI 167= 10=013"
# token = token.replace(" ", "\x01")
# print(token)
# token = bytes(token, encoding="utf-8")
# print(token)
token = scrip_msg()
_logger.debug("sending msg %s" % token)
# symbol = "8=FIXT.1.19=8435=V49=MTC56=MTBM34=150=NSECM924=1115=248=28851775=0263=055=RELIANCE167=10=077"
# symbol = bytes(symbol, encoding="utf-8")
s.sendto(token, address)
print("send %s" % token)

while True:
    data = s.recv(BUFFER_SIZE)
    if data:
        _logger.debug("received %s" % str(data, encoding="utf-8"))
    else:
        s.close()
        break
