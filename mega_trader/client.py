from datetime import datetime

import quickfix as fix
import sys


class Application(fix.Application):
    orderID = 0
    execID = 0

    def gen_ord_id(self):
        global orderID
        orderID += 1
        return orderID

    def onCreate(self, sessionID):
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        return

    def toAdmin(self, sessionID, message):
        return

    def fromAdmin(self, sessionID, message):
        return

    def toApp(self, sessionID, message):
        print("Recieved the following message: %s" % message.toString())
        return

    def fromApp(self, message, sessionID):
        return

    def genOrderID(self):
        self.orderID = self.orderID + 1
        return repr(self.orderID)

    def genExecID(self):
        self.execID = self.execID + 1
        return repr(self.execID)

    def put_order(self):
        print("Creating the following order: ")
        trade = fix.Message()
        print("Trade1: %s" % trade)
        trade.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))  #
        print("Trade2: %s" % trade)
        trade.getHeader().setField(fix.MsgType(fix.MsgType_Logon))  # 35=A
        print("Trade3: %s" % trade)
        trade.setField(fix.ClOrdID(self.genExecID()))  # 11=Unique order
        print("Trade4: %s" % trade)
        trade.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))  # 21=3 (Manual order, best executions)
        print("Trade5: %s" % trade)
        trade.setField(fix.Symbol('HDFCBANK'))  # 55=SMBL ?
        print("Trade6: %s" % trade)
        trade.setField(fix.Side(fix.Side_BUY))  # 43=1 Buy
        print("Trade7: %s" % trade)
        trade.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40=2 Limit order
        print("Trade8: %s" % trade)
        trade.setField(fix.OrderQty(100))  # 38=100
        print("Trade9: %s" % trade)
        trade.setField(fix.Price(10))
        print("Trade10: %s" % trade)
        trade.setField(fix.TransactTime(int(datetime.utcnow().timestamp())))
        print("Trade11: %s " % trade)
        fix.Session_sendToTarget(trade)

    def main(self, config_file):
        try:
            settings = fix.SessionSettings(config_file)
            application = Application()
            storeFactory = fix.FileStoreFactory(settings)
            logFactory = fix.FileLogFactory(settings)
            initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
            initiator.start()

            while 1:
                init_input = input()
                if init_input == '1':
                    print("Putin Order")
                    application.put_order()
                if init_input == '2':
                    sys.exit(0)
                if init_input == 'd':
                    import pdb
                    pdb.set_trace()
                else:
                    print("Valid input is 1 for order, 2 for exit")
                    continue
        except (fix.ConfigError, fix.RuntimeError) as e:
            print(e)


if __name__ == '__main__':
    file_name = "client.cfg"
    application = Application()
    application.main(file_name)
