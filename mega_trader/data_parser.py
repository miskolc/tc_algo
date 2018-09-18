import asyncio
import logging

import quickfix as fix
import quickfix50sp2 as fix50
from model import *

logging.basicConfig(level=ct.log_level)
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
            token_no = int(message.getField(48))
            # LTP
            ltp = float(message.getField(1835))
            # Last Traded Quantity
            ltq = int(message.getField(1843))
            # Last Traded Time
            ltt = str(message.getField(1844))
            # Average Traded Price
            avg_tp = float(message.getField(1845))
            # Open
            scrip_open = float(message.getField(1861))
            # Close
            scrip_close = float(message.getField(1809))
            # High
            scrip_high = float(message.getField(1802))
            # Low
            scrip_low = float(message.getField(1801))
            # Yearly High
            year_high = float(message.getField(1824))
            # Yearly Low
            year_low = float(message.getField(1825))
            # Total Quantity Traded
            volume = int(message.getField(387))
            # Total Trade Value
            turnover = float(message.getField(1840))
            # Percentage Change
            if message.isSetField(1823):
                per_change = (message.getField(1823))
            else:
                per_change = ((ltp - scrip_close) / scrip_close) * 100
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
check_sum_str = "10="


# def read_broadcast_msg(broadcast_message: str):
#     global residue
#     if broadcast_message.__contains__(begin_string_str):
#         broadcast_message.replace(begin_string_str, splitter + begin_string_str)
#         msgs = broadcast_message.split(splitter)
#
#         if residue is None:
#             # Do Nothing
#             pass
#         else:
#             msgs[0] = residue + msgs[0]
#             print(msgs[0])
#             residue = None
#
#         try:
#             if len(msgs) == 1:
#                 print(msgs[0])
#                 # read_msg(msgs[0])
#             elif len(msgs) > 1:
#                 for cmpl_msg in msgs:
#                     try:
#                         print(cmpl_msg)
#                         fix.Message(cmpl_msg, dd, False)
#                         read_msg(cmpl_msg)
#                     except fix.InvalidMessage:
#                         residue = cmpl_msg
#         except fix.InvalidMessage:
#             pass
#     else:
#         if residue is not None:
#             residue += residue
#


async def read_broadcast_msg(broadcast_message: str):
    global residue
    if broadcast_message.__contains__(begin_string_str):
        broadcast_message = broadcast_message.replace(begin_string_str, splitter + begin_string_str)
        msgs = broadcast_message.split(splitter)

        if residue is not None:
            msgs[0] = residue + msgs[0]
            print("Residue and first of next: %s" % msgs[0])
            residue = None

        try:
            if len(msgs) == 1:
                print(msgs[0])
                read_msg(msgs[0])
            elif len(msgs) > 1:
                for cmpl_msg in msgs:
                    if cmpl_msg == '':
                        pass
                    else:
                        try:
                            print("Created: %s" % cmpl_msg)
                            fix.Message(cmpl_msg, dd, False)
                            read_msg(cmpl_msg)
                        except fix.InvalidMessage:
                            residue = cmpl_msg
        except fix.InvalidMessage:
            print("Invalid Message")
    else:
        print("residue is not none: %s" % broadcast_message)
        if residue is not None:
            residue += residue


async def run():
    f = open("C:/Users/sb/PycharmProjects/MyProject/log/msgs.log")
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        print("Original: %s" % line)
        await read_broadcast_msg(line)


asyncio.run(run())
