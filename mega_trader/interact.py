# from quickfix import *
#
# def sendOrderCancelRequest:
#         message = quickfix.Message();
#         header = message.getHeader();
#
#         header.setField(quickfix.BeginString("FIX.4.2"))
#         header.setField(quickfix.SenderCompID(TW))
#         header.setField(quickfix.TargetCompID("TARGET"))
#         header.setField(quickfix.MsgType("D"))
#         message.setField(quickfix.OrigClOrdID("123"))
#         message.setField(quickfix.ClOrdID("321"))
#         message.setField(quickfix.Symbol("LNUX"))
#         message.setField(quickfix.Side(Side_BUY))
#         message.setField(quickfix.Text("Cancel My Order!"))
#
#         Session.sendToTarget(message)
#         fix.Session_sendToTarget(message)
