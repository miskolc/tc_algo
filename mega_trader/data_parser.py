import asyncio
import logging

import quickfix as fix
import quickfix50sp2 as fix50
from model import *

logging.basicConfig(level=ct.log_level, filename="./log/broadcast.log", format="%(asctime)s.%(msecs)03d %(message)s",
                    filemode="w")
_logger = logging.getLogger("mega_trader.data_parser")

dd = fix.DataDictionary("./spec/FIX50SP2.xml")

begin_string = fix.BeginString()
body_length = fix.BodyLength()
message_type = fix.MsgType()
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
check_sum = fix.CheckSum()

TOKEN_NO = 48
LTP = 1835
LTQ = 1843
LTT = 1844
AVG_TP = 1845
OPEN = 1861
CLOSE = 1809
HIGH = 1802
LOW = 1801
YEAR_HIGH = 1824
YEAR_LOW = 1825
VOLUME = 387
TURNOVER = 1840
PERC_CHANGE = 1823


def read_header(message):
    msg_type = None
    _logger.debug("Reading Header")
    if message.getHeader().isSetField(begin_string):
        msg_element = message.getHeader().getField(begin_string)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(body_length):
        msg_element = message.getHeader().getField(body_length)
        _logger.debug(msg_element)
    if message.getHeader().isSetField(message_type):
        msg_element = message.getHeader().getField(message_type)
        msg_type = message.getHeader().getField(message_type).getString()
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
    _logger.debug("Header Read")
    return ct.MsgType(msg_type)


def read_trailer(message):
    if message.getTrailer().isSetField(check_sum):
        msg_element = message.getTrailer().getField(check_sum)
        _logger.debug(msg_element)


def read_tag(message, tag):
    try:
        if message.isSetField(tag):
            msg_value = message.getField(tag)
            # msg_value = message.getField(tag).getString()
            # _logger.debug(msg_element)
            return msg_value
        elif message.getHeader().isSetField(tag):
            msg_element = message.getHeader().getField(tag)
            msg_value = message.getHeader().getField(tag).getString()
            _logger.debug(msg_element)
            return msg_value
        elif message.getTrailer().isSetField(tag):
            msg_element = message.getTrailer().getField(tag)
            msg_value = message.getTrailer().getField(tag).getString()
            _logger.debug(msg_element)
            return msg_value
        else:
            return "0"
    except fix.FieldNotFound:
        return "0"


def read_admin_msg(message):
    msg_type = read_header(message)
    if msg_type == ct.MsgType.HEARTBEAT:
        _logger.debug(msg_type)
    elif ct.MsgType(msg_type) == ct.MsgType.LOGON:
        _logger.debug(msg_type)
    elif msg_type == ct.MsgType.LOGOUT:
        _logger.debug(msg_type)
    elif msg_type == ct.MsgType.REJECT_SESSION_LEVEL:
        _logger.debug(msg_type)
    elif msg_type == ct.MsgType.RESEND_REQUEST:
        _logger.debug(msg_type)
    elif msg_type == ct.MsgType.SEQUENCE_RESET:
        _logger.debug(msg_type)
    elif msg_type == ct.MsgType.SESSION_REJECT:
        _logger.debug(msg_type)
    elif msg_type == ct.MsgType.TEST_REQUEST:
        _logger.debug(msg_type)
    else:
        _logger.warning("Not found")
        _logger.info(msg_type)


def read_app_msg(message):
    try:
        msg_type = read_header(message)
        _logger.debug(msg_type)
        if (msg_type == ct.MsgType.AUCTION_ACTIVITY_MESSAGE) | (msg_type == ct.MsgType.BCD):
            _logger.debug("Unwanted message not parsed")
            pass
        elif msg_type == ct.MsgType.INDEX_BROADCAST:
            pass
            # print("Index Broadcast")
            # No. of Records, 1828
            # noIndexRecords = int(message.getField(1828))
            # if noIndexRecords > 0:
            #     group = fix.Group(1828, 1826, )
            #     #     # group = fix.Group(1828, 1827, [1826,1815,1816,1817,1818,1819,1820,1821,1822,1823,1824,1825,1827])
            #     message.getGroup(num=1, group=group)
            #
            # # Index Name, 1826
            # message.getField(1826)
            # # Open Index, 1815
            # message.getField(1815)
            # # High Index, 1816
            # message.getField(1816)
            # # Low Index, 1817
            # message.getField(1817)
            # # Close Index, 1818
            # message.getField(1818)
            # # Index Value, 1819
            # message.getField(1819)
            # # Market Capitalization, 1820
            # message.getField(1820)
            # # No. of Down Moves, 1821
            # message.getField(1821)
            # # No. of Up Moves, 1822
            # message.getField(1822)
            # # Percentage Change, 1823
            # message.getField(1823)
            # # Yearly High, 1824
            # message.getField(1824)
            # # Yearly Low, 1825
            # message.getField(1825)
            # # Net Change Indicator, 1827
            # message.getField(1827)
        elif msg_type == ct.MsgType.MARKET_PICTURE:
            # Token No.
            token_no = int(read_tag(message, TOKEN_NO))
            # LTP
            ltp = float(read_tag(message, LTP))
            # Last Traded Quantity
            ltq = int(read_tag(message, LTQ))
            # Last Traded Time
            ltt = str(read_tag(message, LTT))
            # Average Traded Price
            avg_tp = float(read_tag(message, AVG_TP))
            # Open
            scrip_open = float(read_tag(message, OPEN))
            # Close
            scrip_close = float(read_tag(message, CLOSE))
            # High
            scrip_high = float(read_tag(message, HIGH))
            # Low
            scrip_low = float(read_tag(message, LOW))
            # Yearly High
            year_high = float(read_tag(message, YEAR_HIGH))
            # Yearly Low
            year_low = float(read_tag(message, YEAR_LOW))
            # Total Quantity Traded
            volume = int(read_tag(message, VOLUME))
            # Total Trade Value
            turnover = float(read_tag(message, TURNOVER))
            # Percentage Change
            if message.isSetField(PERC_CHANGE):
                per_change = (message.getField(PERC_CHANGE))
            else:
                try:
                    per_change = ((ltp - scrip_close) / scrip_close) * 100
                except (ValueError, TypeError, ZeroDivisionError):
                    per_change = None
            # noMDEntries = fix.NoMDEntries()
            # entries = int(message.getField(noMDEntries).getString())
            # group = fix50.MarketDataSnapshotFullRefresh.NoMDEntries()
            # MDEntryType = fix.MDEntryType()
            # MDEntryPx = fix.MDEntryPx()
            # MDEntrySize = fix.MDEntrySize()
            # orderID = fix.OrderID()
            # print(entries)
            # i = 1
            # while i <= entries:
            #     print(i)
            #     message.getGroup(i, group)
            #     i += 1
            # print(group.getField(MDEntryType))
            # group.getField(MDEntryPx)
            # group.getField(MDEntrySize)
            # group.getField(orderID)
            data = ScripData(token=token_no, open=scrip_open, high=scrip_high, low=scrip_low, close=scrip_close,
                             ltp=ltp, time=ltt, turnover=turnover, volume=volume, per_change=per_change,
                             year_high=year_high, year_low=year_low)
            print(data)

    except (ValueError, fix.FieldNotFound) as e:
        _logger.warning("Error %s" % e)
        _logger.info("Error occured for message type: %s" % message.getHeader().getField(35))


def read_msg(message):
    try:
        rec = fix.Message(message, dd, False)
        if rec.isAdmin():
            read_admin_msg(rec)
        elif rec.isApp():
            read_app_msg(rec)
    except fix.InvalidMessage as e:
        _logger.warning("Error %s" % e)
        _logger.info("Error while reading message: %s" % message)


residue = None
begin_string_str = "8=FIXT.1.1"
splitter = "*&"


async def read_broadcast_msg(broadcast_message: str):
    global residue
    if broadcast_message.__contains__(begin_string_str):
        broadcast_message = broadcast_message.replace(begin_string_str, splitter + begin_string_str)
        msgs = broadcast_message.split(splitter)

        if residue is not None:
            msgs[0] = residue + msgs[0]
            _logger.debug("Residue and first of next: %s" % msgs[0])
            residue = None

        try:
            if len(msgs) == 1:
                _logger.info(msgs[0])
                read_msg(msgs[0])
            elif len(msgs) > 1:
                for cmpl_msg in msgs:
                    if cmpl_msg == '':
                        pass
                    else:
                        try:
                            _logger.info("Created: %s" % cmpl_msg)
                            fix.Message(cmpl_msg, dd, False)
                            read_msg(cmpl_msg)
                        except fix.InvalidMessage:
                            residue = cmpl_msg
        except fix.InvalidMessage:
            _logger.warning("Invalid Message")
    else:
        _logger.debug("residue is not none: %s" % broadcast_message)
        if residue is not None:
            residue += residue


async def run():
    f = open("C:/Users/sb/PycharmProjects/MyProject/log/msgs.log")
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        _logger.info("Original: %s" % line)
        await read_broadcast_msg(line)


def analyse(broadcast_message):
    asyncio.run(read_broadcast_msg(broadcast_message))
