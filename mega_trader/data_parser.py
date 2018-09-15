import logging

import quickfix as fix
from model import *

logging.basicConfig(level=ct.log_level)
_logger = logging.getLogger("mega_trader.data_parser")


def read_header(message):
    message_type = None
    begin_string = fix.BeginString()
    body_length = fix.BodyLength()
    msg_type = fix.MsgType()
    sender_id = fix.SenderCompID()
    target_id = fix.TargetCompID()
    msg_seq = fix.MsgSeqNum()
    sender_sub_id = fix.SenderSubID()
    target_sub_id = fix.TargetSubID()
    duplicate_flag = fix.PossDupFlag()
    user_req_type = fix.UserRequestType()
    gateway_id = fix.MarketID()
    orig_sending_time = fix.OrigSendingTime()
    sending_time = fix.SendingTime()
    on_behalf_id = fix.OnBehalfOfCompID()

    if message.getHeader().isSetField(begin_string):
        msg_element = message.getHeader().getField(begin_string)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(body_length):
        msg_element = message.getHeader().getField(body_length)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(msg_type):
        msg_element = message.getHeader().getField(msg_type)
        message_type = message.getHeader().getField(msg_type).getString()
        _logger.debug(msg_element)
    if message.getHeader().isSetField(sender_id):
        msg_element = message.getHeader().getField(sender_id)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(target_id):
        msg_element = message.getHeader().getField(target_id)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(msg_seq):
        msg_element = message.getHeader().getField(msg_seq)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(sender_sub_id):
        msg_element = message.getHeader().getField(sender_sub_id)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(target_sub_id):
        msg_element = message.getHeader().getField(target_sub_id)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(duplicate_flag):
        msg_element = message.getHeader().getField(duplicate_flag)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(user_req_type):
        msg_element = message.getHeader().getField(user_req_type)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(gateway_id):
        msg_element = message.getHeader().getField(gateway_id)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(orig_sending_time):
        msg_element = message.getHeader().getField(orig_sending_time)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(sending_time):
        msg_element = message.getHeader().getField(sending_time)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(on_behalf_id):
        msg_element = message.getHeader().getField(on_behalf_id)
        _logger.debug(msg_element)
    return ct.MsgType(message_type)


def read_trailer(message):
    check_sum = fix.CheckSum()
    if message.getTrailer().isSetField(check_sum):
        msg_element = message.getTrailer().getField(check_sum)
        print(msg_element)


def read_admin_msg(message):
    msg_type = read_header(message)
    if msg_type == ct.MsgType.HEARTBEAT:
        print(msg_type)
    elif ct.MsgType(msg_type) == ct.MsgType.LOGON:
        print(msg_type)
    elif msg_type == ct.MsgType.LOGOUT:
        print(msg_type)
    elif msg_type == ct.MsgType.REJECT_SESSION_LEVEL:
        print(msg_type)
    elif msg_type == ct.MsgType.RESEND_REQUEST:
        print(msg_type)
    elif msg_type == ct.MsgType.SEQUENCE_RESET:
        print(msg_type)
    elif msg_type == ct.MsgType.SESSION_REJECT:
        print(msg_type)
    elif msg_type == ct.MsgType.TEST_REQUEST:
        print(msg_type)
    else:
        print("Not found")
        print(msg_type)


def read_app_msg(message):
    msg_type = read_header(message)
    print(msg_type)


received = "8=FIXT.1.19=108135=IB49=NSECM56=MTBM34=1924=1115=21828=61826=Nifty CPSE1815=2294.51816=2310.151817=2286.551818=2276.751819=2294.21820=1967852601488651821=262231822=257851823=0.771824=2799.551825=2139.51827=-1826=Nifty GrowSect 151815=7037.751816=7070.351817=7023.651818=6990.61819=7042.91820=7768216282514231821=782041822=750561823=0.751824=7354.551825=5942.151827= 1826=Nifty50 Value 201815=5444.71816=5465.61817=5417.41818=5413.61819=5425.91820=1.90667550936387E+151821=1348851822=1341791823=0.231824=5563.81825=4171.651827=-1826=Nifty Mid Liq 151815=4133.551816=4206.551817=4133.551818=4107.21819=4205.41820=1573956262705091821=428041822=442911823=2.391824=4677.051825=3770.551827=-1826=Nifty Pvt Bank1815=15385.21816=15415.51817=15339.751818=15248.81819=15377.71820=9015155094048031821=589741822=592681823=0.851824=16152.151825=13298.31827=+1826=NIFTY MIDCAP 1001815=19184.851816=19326.31817=19184.851818=19046.551819=19314.251820=7127426889917151821=1858871822=1884631823=1.411824=21840.851825=17700.91827=-10=174"
dd = fix.DataDictionary("./spec/FIX50SP2.xml")

# f = open("test-log.log", "r")
# lines = f.readlines()
# line = lines[0]
# print(line)
rec = fix.Message(received, dd, False)
if rec.isAdmin():
    read_admin_msg(rec)
else:
    read_app_msg(rec)
# print(lines)

# for line in lines:
#     rec = fix.Message(line, dd, False)
#     if rec.isAdmin():
#         read_admin_msg(rec)
#     else:
#         read_app_msg(rec)
# print(line)
# read_header(rec)
# read_trailer(rec)
