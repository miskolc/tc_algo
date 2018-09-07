import argparse
import logging
import time
from datetime import datetime

import quickfix as fix
import sys

_logger = logging.getLogger("mega_trader.client")


# noinspection PyPep8Naming
class ClientApplication(fix.Application, fix.Message):
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

    def onLogon(self, sessionID: fix.SessionID):
        self.session_id = sessionID
        _logger.info(sessionID)
        print("Successful Logon to session(Active Session) '%s'." % sessionID)
        return

    def onLogout(self, sessionID: fix.SessionID):
        print("Logout from session: %s" % sessionID)
        return

    def toAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        print("To admin: %s" % message)
        return

    def fromAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        print("From admin: %s" % message)
        return

    def toApp(self, message: fix.Message, sessionID: fix.SessionID):
        print("Recieved the following message: %s" % message)
        return

    def fromApp(self, message: fix.Message, sessionID: fix.SessionID):
        print("Response: %s" % message)
        return

    def genOrderID(self):
        self.orderID = self.orderID + 1
        return repr(self.orderID)

    def genExecID(self):
        self.execID = self.execID + 1
        return repr(self.execID)


if __name__ == '__main__':
    try:
        file_name = "client.cfg"
        settings = fix.SessionSettings(file_name)
        store_factory = fix.FileStoreFactory(settings)
        log_factory = fix.FileLogFactory(settings)
        _client = ClientApplication()
        initiator = fix.SocketInitiator(_client, store_factory, settings, log_factory)
        initiator.start()
        logon = fix.Message()
        logon.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        logon.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
        logon.setField(fix.Username("AP"))
        logon.setField(fix.EncryptMethod(0))
        fix.Session.sendToTarget(logon, _client.session_id)
        # _client.onLogon(_client.session_id)
        # while True:
        #     input_value = int(input())
        #     if input_value == 1:
        #         if initiator.isLoggedOn():
        #             print("logged")
        #         else:
        #             print(initiator)
        #         logon = fix.Message()
        #         logon.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
        #         logon.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
        #         logon.setField(fix.Username("AP"))
        #         logon.setField(fix.EncryptMethod(0))
        #         message = logon.toString()
        #         print(_client.session_id)
        #         fix.Session.sendToTarget(logon, _client.session_id)
        #     else:
        #         initiator.stop()
        #         break

        # while True:
        #     in_res = int(input())
        #     if in_res == 1:
        #         message = fix.Message()
        #         message.setField(fix.MDReqID('1'))
        #         message.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))
        #         message.setField(fix.MarketDepth(0))
        #         message.setField(fix.NoMDEntryTypes(2))
        #         message.setField(fix.MDUpdateType(fix.MDUpdateType_INCREMENTAL_REFRESH))
        #     else:
        #         initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
