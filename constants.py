"""
Constants used in the modules
Don't change these values. It might break the code.
"""
import logging
from enum import Enum

default = "null"
log_level = logging.DEBUG


class Keys:
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'
    yearly = 'yearly'
    interval = 'interval'
    scrip = 'scrip'
    symbol = 'symbol'
    size = 'size'
    start_date = 'start_date'
    end_date = 'end_date'
    chart = 'chart'
    bt_chart = 'bt_chart'
    date = 'date'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    turnover = 'turnover'

    rsi = "RSI"
    stoch = "STOCH"
    fastk = "fastk"
    fastd = "fastd"
    sma = "SMA"
    ema = "EMA"
    macd = "MACD"
    macd_value = "macd_value"
    macdsignal = "macdsignal"
    macdhist = "macdhist"
    bbands = "BBANDS"
    upperband = "upperband"
    middleband = "middleband"
    lowerband = "lowerband"
    pivot = "PIVOT"
    pp = "pp"
    r1 = "r1"
    r2 = "r2"
    r3 = "r3"
    s1 = "s1"
    s2 = "s2"
    s3 = "s3"
    data_min = "data_min"
    data_max = "data_max"
    pivot_min = "pivot_min"
    pivot_max = "pivot_max"

    signal = 'Signal'
    quantity = 'QTY'
    price = 'Price'
    pl = 'P_L'
    cum_pl = 'CUM_P_L'
    date_cum_pl = 'DATE_CUM_PL'
    data_prop = 'data_properties'
    data = 'data'
    params = 'params'
    patterns = "patterns"
    all = 'all'
    long = 'long'
    short = 'short'
    annotations = 'annotations'
    buy_regular = "BR"
    buy_book_profit = "BP"
    buy_book_sl = "BSL"
    sell_regular = "SR"
    sell_book_profit = "SP"
    sell_book_sl = "SSL"

    call = "CE"
    put = "PE"
    buy = "buy"
    sell = "sell"


class MsgType(Enum):
    # Unwanted Messages
    BCD = "BCD"
    # ADMINISTRATIVE MESSAGE
    HEARTBEAT = "0"
    LOGON = "A"
    LOGOUT = "5"
    REJECT_SESSION_LEVEL = "3"
    RESEND_REQUEST = "2"
    SEQUENCE_RESET = "4"
    SESSION_REJECT = "3"
    TEST_REQUEST = "1"
    # INTERACTIVE MESSAGE
    ACCOUNT_MAPPING = "AM"
    BUSINESS_MESSAGE_REJECT = "j"
    CLIENT_MAPPING = "MP"
    DOWNLOAD_DATA = "DD"
    DOWNLOAD_NOTIFICATION = "DN"
    MARGIN_CHANGE = "CJ"
    MULTI_LEG_ORDER_REQUEST = "MER"
    ORDER_REQUEST = "D"
    ORDER_PAIR_TYPE = "OP"
    PARTY_RIK_LIMIT_REPORT = "PRL"
    PARTY_RIK_LIMIT_REPORT_UPDATE = "PRLU"
    RMS_DETAIL_INFO = "CR"
    RMS_DETAILS_UTILIZED_RESPONSE = "CU"
    RMS_INFO = "CM"
    RMS_UTILIZED_REQUEST = "CS"
    RMS_UTILIZED_RESPONSE = "CT"
    SECURITY_DEFINITION = "C"
    SECURITY_DEFINITION_INFO = "d"
    STRATEGY_MAPPING = "CD"
    SYSTEM_INFORMATION = "SI"
    TRADING_SESSION_STATUS = "h"
    NO_OF_ALLOWED_GATEWAY = ""
    # BROADCAST MESSAGES
    DPR_CHANGE_NOTIFICATION = "z"
    EXCHANGE_MESSAGE = "EM"
    INDEX_BROADCAST = "IB"
    MARKET_PICTURE = "W"
    MARKET_WIDE_LIMIT = "MWL"
    MOST_ACTIVE_CONTRACT_BY_VOLUME_AND_VALUE_INFO = "MAC"
    NEWS = ""
    OPEN_INTEREST = "OI"
    SECURITY_STATUS = "f"
    SPREAD_MARKET_PICTURE = "SMP"
    TBT_TRADE_DETAILS = ""
    TOKEN_REQUEST = "V"
    TOP_GAINER_LOSER = "TGL"
    # NESTED STRUCTURE
    CLIENT_CODE_GRP = ""
    DP_STOCK_DETAIL = ""
    EXCHANGE_MARGIN_DETAIL = ""
    GATEWAY_ID_GRP = ""
    INSTRUMENT = ""
    INSTRUMENT_DETAIL = ""
    LEG_GRP = ""
    MD_ENTRY_GRP = ""
    MOST_ACTIVE_INSTRUMENT_INFO = ""
    NO_INDEX_RECORD = ""
    NO_LINES_OF_TEXT = ""
    NO_RELATED_SYM_NEWS = ""
    NO_UNDERLYING = ""
    TOP_GAINER_LOSER_INSTRUMENT_INFO = ""
    # AUCTION
    AUCTION_ACTIVITY_MESSAGE = "AAM"
    AUCTION_ENQUIRY_DATA = ""
    AUCTION_ENQUIRY_REQUEST = ""
    AUCTION_STATUS = ""
    BSE_AUCTION_MARKET_PICTURE = ""
    BSE_AUCTION_REQUEST = ""
    BSE_MARKET_PICTURE_REPEATING_GRP = ""
    # SERVICE
    ACC_UNLOCK = ""
    DP_STOCK_REQUEST = ""
    DP_STOCK_RESPONSE = ""
    MARGIN_DETAIL = ""
    SERVICE_LOG_OFF = ""
    SERVICE_LOGON = ""
    # SYSTEM MESSAGE
    INFO_MESSAGE = ""

    def __str__(self):
        return self.value


class OrderStatus(Enum):
    SUBMITTED = "1"
    M_PENDING = "2"
    E_PENDING = "3"
    FREEZED = "4"
    M_REJECTED = "5"
    E_REJECTED = "6"
    CANCELLED = "7"
    E_CANCELLED = "8"
    EXECUTED = "9"
    ES_ORDER = "A"
    ES_TRADE = "B"
    SL_PENDING = "S"


class BookType(Enum):
    RL = "1"
    ST = "2"
    SL = "3"
    MKT = "4"
    MIT = "5"
    AUC_BUY_IN = "6"
    AUC_SELL_IN = "7"
    AUC_TRADING_BUY_IN = "8"
    AUC_TRADING_SELL_IN = "9"
    AU = "A"


class ValidityType(Enum):
    AON = "1"
    IOC = "2"
    GTC = "3"
    DAY = "4"
    GTD = "5"
    EOS = "6"
    FOK = "7"
    GTT = "8"


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


class DbIndex(Enum):
    """
    This enums are used for the indexing the database columns for FO data
    """
    index_id = 0
    instrument_id = 1
    symbol_id = 2
    expiry_id = 3
    strike_id = 4
    option_type_id = 5
    open_id = 6
    high_id = 7
    low_id = 8
    close_id = 9
    settle_id = 10
    contracts_id = 11
    val_id = 12
    open_int_id = 13
    chg_in_oi = 14
    timestamp_id = 15

    def __str__(self):
        return self.value


class ApiKeys:
    key_config = 'config'
    key_credentials = 'credentials'
    key_login_id = 'LoginId'
    key_password = 'Password'
    key_api = 'api'
    key_unique_id = 'UniqueId'
    key_ref_no = 'RefNo'
    key_modified = "Modified"
    unique_id = 'UniqueId'
    ref_no = 'RefNo'
    gateway = "gateway"
    exchange = "Exchange"
    token_no = "Tokenno"
    client_code = "clientcode"
    buy_sell = "Buysell"
    qty = "qty"
    price = "price"
    trigger_price = "Triggerprice"
    book_type = "Booktype"
    validity = "validity"
    error = 'Error'


class OrderKeys:
    BUY = "BUY"
    SELL = "SELL"
    RL = "RL"
    SL = "SL"
    DAY = "DAY"
    IOC = "IOC"
    FOK = "FOK"
