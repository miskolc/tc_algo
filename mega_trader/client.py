import argparse
import logging
import time
from datetime import datetime

import quickfix as fix
import quickfix50sp2 as fix50
import sys

_logger = logging.getLogger("mega_trader.client")


# noinspection PyPep8Naming
class ClientApplication(fix.Application, fix50.Message):
    orderID = 0
    execID = 0
    session_id = None
    initiator = None

    def gen_ord_id(self):
        global orderID
        orderID += 1
        return orderID

    def onCreate(self, sessionID: fix.SessionID):
        self.session_id = sessionID
        print("Session created: %s" % sessionID)
        return

    def onLogon(self, session_id):
        self.session_id = session_id
        _logger.info(session_id)
        print("Successful Logon to session(Active Session) '%s'." % session_id)
        return

    def onLogout(self, session_id):
        print("Logout from session: %s" % session_id)
        return

    def toAdmin(self, message: fix.Message, session_id):
        print("To admin: %s" % message)
        return

    def fromAdmin(self, message: fix.Message, session_id):
        TradeID = fix.TradingSessionID
        message.getField(TradeID)
        print("From admin: %s" % message)
        return

    def toApp(self, message: fix.Message, session_id):
        print("Recieved the following message: %s" % message)
        return

    def fromApp(self, message: fix.Message, session_id):
        print("Response: %s" % message)
        return

    def genOrderID(self):
        self.orderID = self.orderID + 1
        return repr(self.orderID)

    def genExecID(self):
        self.execID = self.execID + 1
        return repr(self.execID)

    def onMessage(self, message, sessionID):
        print(message)

    def logon_msg(self):
        logon_req = fix.Message()
        logon_req.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        logon_req.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
        logon_req.setField(fix.SenderCompID("AP"))
        logon_req.setField(fix.TargetCompID("MTBM"))
        logon_req.setField(fix.MsgSeqNum(1))
        logon_req.setField(fix.UserRequestType(1))
        logon_req.setField(fix.HeartBtInt(1))
        logon_req.setField(fix.Username("AP"))
        logon_req.setField(932, "14")
        logon_req.setField(fix.DefaultApplVerID(fix.ApplVerID_FIX50SP2))
        logon_req.setField(1701, "1")
        group = fix50.MarketDataSnapshotFullRefresh
        logon_req.setField(1301, "1")
        # group.setField(1301, "2")
        # group.setField(1301, "4")
        # group.setField(1301, "16")
        # group.setField(1301, "2048")
        # group.setField(1301, "32768")
        # logon_req.setField(1301, "16777216")
        # logon_req.addGroup(group)
        logon_req.setField(1137, "FIX.5.0SP2")
        print(logon_req)
        logon_req = bytes(logon_req.toString(), encoding="UTF-8")
        return logon_req

    def run(self):
        print("run")
        fix.Session_sendToTarget(self.logon_msg(), _client.session_id)
        print("message send")
        while True:
            print("Reading...")


if __name__ == '__main__':
    try:
        file_name = "client.cfg"
        settings = fix.SessionSettings(file_name)
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        _client = ClientApplication()
        initiator = fix.SocketInitiator(_client, store_factory, settings, log_factory)
        print("initiated")
        initiator.start()
        _client.run()
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
