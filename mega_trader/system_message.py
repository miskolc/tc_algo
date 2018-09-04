from enum import Enum


class InfoMessage(Enum):
    MessageType = 1473
    Message = 1830
    ApplId = 1180
    ApplSeqNum = 1181
    Headline = 148
    LastRepRequested = 912
    OrigTime = 42
    Urgency = 61


class Gateway(Enum):
    NSEFO = 1
    NSECM = 2
    eFips = 3
    NSECD = 4
    BSEINX = 5
    NCDEX = 8
    BSE = 16
    BSEFO = 32
    MCX = 64
    MCXSX = 128
    MCXSXFO = 256
    MCXSXCM = 512
    ICEX = 1024
    DGCX = 2048
    VERTEX = 2049
    BFX = 4096
    SMX = 8192
    GBOT = 16384
    TTFIX = 32768
    XTRADER = 65536
    NDF = 131072
    CME = 262144
    SGX = 524288
    MT = 1048576
    FXCM = 2097152
    RTS = 4194304
    CTP = 8388608
    BSECD = 16777216


class MessageType(Enum):
    Heartbeat = 0
    Test_Request = 1
    Resend_Request = 2
    Reject = 3
    Sequence_Reset = 4
    Logout = 5
    Execution_Report = 8
    Order_cancel_reject = 9
    Logon = "A"
    News = "B"
    New_Order_Single = "D"
    New_Order_MultiLeg = "AB"
    Order_Cancel_Request = "F"
    Order_Cancel_Replace_Request = "G"
    Business_Reject_Message = "J"
    Order_Mass_Cancel_Request = "Q"
    Order_Mass_Cancel_Reject = "R"
