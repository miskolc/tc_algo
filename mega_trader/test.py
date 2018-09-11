import socket
import sys

import quickfix as fix
import quickfix50sp2 as fix50
import logging

logging.basicConfig(level=logging.DEBUG, filename="./broadcast.log", filemode="w",
                    format="%(asctime)s:%(message)s")
_logger = logging.getLogger("test")
fmt = logging.Formatter("%(message)s")
handler = logging.FileHandler(filename="./messages.log", mode="w")
handler.setFormatter(fmt)
_message_log = logging.getLogger("msg")
_message_log.addHandler(handler)


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
    # 8, BeginString
    scrip.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
    # 35, Message Type
    scrip.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
    # 49, SenderCompId
    scrip.getHeader().setField(fix.SenderCompID("AP"))
    # 56, TargetCompId
    scrip.getHeader().setField(fix.TargetCompID("MTBM"))
    # 34, Message SeqNumber
    scrip.setField(fix.MsgSeqNum(1))
    # 50, SenderSubID
    scrip.setField(fix.SenderSubID("NSECM"))
    # 924, UserRequestType
    scrip.setField(fix.UserRequestType(1))
    # 115 ,doubtful, but may be gateway id according to examples
    # NSECM = 2, NSEFO = 1
    scrip.setField(115, "1")
    # 55, Symbol
    scrip.setField(fix.Symbol("RELIANCE"))
    # 1775, price divisor
    scrip.setField(1775, "0")
    # 167, Instrument
    scrip.setField(167, "")
    # 48, Token No.
    scrip.setField(48, "2885")
    scrip.setField(263, "0")
    print(scrip)
    scrip = bytes(scrip.toString(), encoding="UTF-8")
    return scrip


TCP_IP = '192.168.6.107'
TCP_PORT = 2002
BUFFER_SIZE = 1024 * 10
address = (TCP_IP, TCP_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

logon = logon_msg()
s.sendto(logon, address)

token = scrip_msg()
s.sendto(token, address)

arr = []
long_str = ""
i = 0
while i < 100:
    data = s.recv(BUFFER_SIZE)
    if data:
        temp = str(data, encoding="UTF-8")
        arr.append(temp)
        long_str = long_str + temp
        i += 1
        _logger.debug("IN %s" % str(data, encoding="utf-8"))
    else:
        s.close()
        break

s.close()

# long_str = long_str.replace("8=FIXT.1.1", "*&8=FIXT.1.1")
# arr1 = long_str.split("*&")
# for j in arr1:
#     _message_log.debug(j)
