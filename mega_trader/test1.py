import quickfix as fix
import quickfix50sp2 as fix50

token1 = "8=FIXT.1.19=8435=V49=MTC56=MTBM34=150=NSECM924=1115=248=28851775=0263=055=RELIANCE167=10=077"
token = fix.Message()
token.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
token.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
token.getHeader().setField(fix.SenderCompID("AP"))
token.getHeader().setField(fix.TargetCompID("MTBM"))
token.setField(fix.MsgSeqNum(1))
token.setField(fix.SenderSubID("NSECM"))
token.setField(fix.UserRequestType(1))
token.setField(115, "1")
token.setField(fix.Symbol("RELIANCE"))
token.setField(1775, "0")
token.setField(167, "")
token.setField(48, "1333")
token.setField(263, "0")
print(token)
# print(bytes(token.toString(), encoding="UTF-8"))


# logon1 = "8=FIXT.1.1\x019=140\x0135=A\x0149=AP\x0156=MTBM\x0134=1\x01924=1\x01108=1\x01553=AP\x01932=14\x011137=FIX.5" \
#         ".0SP2\x011701=7\x011301=16777216\x011301=2048\x011301=1\x01\x01301=4\x011301=2\x011301=32768" \
#         "\x011301=16\x0110=107\x01 "
#
# logon_req = fix.Message()
# logon_req.getHeader().setField(fix.BeginString(fix.BeginString_FIXT11))
# logon_req.getHeader().setField(fix.MsgType(fix.MsgType_Logon))
# logon_req.setField(fix.SenderCompID("AP"))
# logon_req.setField(fix.TargetCompID("MTBM"))
# logon_req.setField(fix.MsgSeqNum(1))
# logon_req.setField(fix.UserRequestType(1))
# logon_req.setField(fix.HeartBtInt(1))
# logon_req.setField(fix.Username("AP"))
# logon_req.setField(fix.NetworkResponseID("14"))
# logon_req.setField(fix.DefaultApplVerID(fix.ApplVerID_FIX50SP2))
# logon_req.setField(1701, "7")
# group = fix50.MarketDataSnapshotFullRefresh()
# group.setField(fix.MarketID("1"))
# group.setField(fix.MarketID("2"))
# group.setField(fix.MarketID("4"))
# group.setField(fix.MarketID("16"))
# group.setField(fix.MarketID("2048"))
# group.setField(fix.MarketID("32768"))
# group.setField(fix.MarketID("16777216"))
# # logon_req.addGroup(group)
# logon_req.setField(1137, "FIX.5.0SP2")
# print(logon_req)
# logon = bytes(logon_req.toString(), encoding="UTF-8")
# print(logon)
