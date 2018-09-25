import logging.handlers
import socket

import quickfix as fix

from model import *
from mega_trader import mt_data_parser

logging.basicConfig(level=ct.log_level, format="%(asctime)s:%(message)s")
_logger = logging.getLogger("client")
_logger.propagate = False

broadcast_handler = logging.handlers.RotatingFileHandler(filename="./log/broadcast.log", mode="a",
                                                         maxBytes=5 * 1024 * 1024, backupCount=50)
fmt = logging.Formatter("%(asctime)s:%(message)s")
broadcast_handler.setFormatter(fmt)
broadcast_handler.setLevel(logging.DEBUG)
_broadcast_logger = logging.getLogger("client.broadcast")
_broadcast_logger.propagate = False
_broadcast_logger.addHandler(broadcast_handler)

message_handler = logging.handlers.RotatingFileHandler(filename="./log/messages.log", mode="a",
                                                       maxBytes=5 * 1024 * 1024, backupCount=50)
fmt = logging.Formatter("%(message)s")
message_handler.setFormatter(fmt)
message_handler.setLevel(logging.DEBUG)
_message_logger = logging.getLogger("client.message")
_message_logger.propagate = False
_message_logger.addHandler(message_handler)

TCP_IP = '192.168.6.107'
TCP_PORT = 2002
BUFFER_SIZE = 1024 * 10
address = (TCP_IP, TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sender_id = "TC"
target_id = "MTM"
user = "TC"
response = 0


def client_logon(sender: str, target: str, username: str, scrips: list = None, response_id: int = None):
    # noinspection PyArgumentList
    def logon_msg(sender_comp_id, target_comp_id, username_client, response_id_network):
        if response_id_network is None:
            response_id_network = int((numpy.random.random()) * 100000)
        _message_logger.info("Logon with response id: %s" % response_id_network)
        _message_logger.debug("Building logon message")
        logon_req = fix.Message()
        logon_req.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        logon_req.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
        logon_req.setField(fix.SenderCompID(sender_comp_id))
        logon_req.setField(fix.TargetCompID(target_comp_id))
        logon_req.setField(fix.MsgSeqNum(1))
        logon_req.setField(fix.UserRequestType(1))
        logon_req.setField(fix.HeartBtInt(1))
        logon_req.setField(fix.Username(username_client))
        logon_req.setField(fix.NetworkResponseID("%s" % response_id_network))
        logon_req.setField(fix.DefaultApplVerID(fix.ApplVerID_FIX50SP2))
        logon_req.setField(1701, "1")
        logon_req.getTrailer().setField(fix.MarketID("2"))
        logon_req.setField(fix.DefaultApplVerID("FIX.5.0SP2"))
        logon_req = bytes(logon_req.toString(), encoding="UTF-8")
        _message_logger.debug("Logon message built")
        return logon_req

    # noinspection PyArgumentList
    def scrip_msg(scrip_element: Scrip):
        scrip_subscription = fix.Message()
        # 8, BeginString
        scrip_subscription.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        # 35, Message Type
        scrip_subscription.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
        # 49, SenderCompId
        scrip_subscription.getHeader().setField(fix.SenderCompID(sender_id))
        # 56, TargetCompId
        scrip_subscription.getHeader().setField(fix.TargetCompID(target_id))
        # 34, Message SeqNumber
        scrip_subscription.setField(fix.MsgSeqNum(1))
        # 50, SenderSubID
        scrip_subscription.setField(fix.SenderSubID(scrip_element.exchange))
        # 924, UserRequestType
        scrip_subscription.setField(fix.UserRequestType(1))
        # 115 ,doubtful, but may be gateway id according to examples
        # NSECM = 2, NSEFO = 1
        scrip_subscription.setField(115, "%s" % scrip_element.gatewayID)
        # 55, Symbol
        scrip_subscription.setField(fix.Symbol(scrip_element.symbol))
        # 1775, price divisor
        scrip_subscription.setField(1775, "0")
        # 167, Instrument
        scrip_subscription.setField(167, scrip_element.instrument)
        # 48, Token No.
        scrip_subscription.setField(48, "%s" % scrip_element.token_no)
        # 263, Broadcast type
        scrip_subscription.setField(263, "0")
        scrip_subscription = bytes(scrip_subscription.toString(), encoding="UTF-8")
        return scrip_subscription

    def send(message: bytes):
        s.sendto(message, address)

    s.connect(address)
    logon = logon_msg(sender, target, username, response_id)
    send(logon)

    if scrips is not None:
        for scrip in scrips:
            _message_logger.debug("Sending %s" % scrip)
            token = scrip_msg(scrip)
            s.sendto(token, address)
            _message_logger.debug("Send %s" % scrip)

    try:
        while True:
            data = s.recv(BUFFER_SIZE)
            if data:
                msg = str(data, encoding="UTF-8")
                _broadcast_logger.debug("%s" % str(data, encoding="utf-8"))
                mt_data_parser.analyse(msg)
            else:
                s.close()
                break
    except socket.error as e:
        print("Following error occurred:")
        print(e)
    finally:
        s.close()
    s.close()
