# TODO: For any reference contact or see cond.js
import logging

import plotly.plotly
import plotly.graph_objs as go

import constants
import data_parser
import indicators
from model import *

_logger = logging.getLogger("strategy")
BUY = "buy"
SELL = "sell"
TARGET = "target"
SL = "sl"
auto_op = Logical.AND


class Strategies:
    """
    All pre-defined strategies.
    """
    @staticmethod
    def ma(data: list, data_properties: dict, ma_type: int = 0) -> dict:
        """
        Strategy for moving averages.
        :param data: list[numeric]
        :param data_properties: dict
        :param ma_type: Moving Average Type
                SMA = 0
                EMA = 1
        :return: dict
                Result from strategy_builder
        """
        close = data_parser.get_close(data)
        if ma_type == 1:
            ma50 = indicators.ema(close, period=50)
            ma200 = indicators.ema(close, period=200)
        else:
            ma50 = indicators.sma(close, period=50)
            ma200 = indicators.sma(close, period=200)
        buy = Condition(data1=ma50, data2=ma200, operation=Operation.CROSSOVER)
        sell = Condition(data1=ma50, data2=ma200, operation=Operation.CROSSUNDER)
        chart_1 = ChartElement(data=ma50, label="ma50", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                               color=ChartColor.GREEN)
        chart_2 = ChartElement(data=ma200, label="ma200", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                               color=ChartColor.RED)
        charts = [chart_1, chart_2]
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=BUY, buy=buy, sell=sell,
                                  charts=charts)
        show_back_testing_reports(result)
        return result

    @staticmethod
    def macd(data: list, data_properties: dict) -> dict:
        """
        Strategy for Moving Average Convergence/Diversion.
        :param data: list[numeric]
        :param data_properties: dict
        :return: dict
                Result from strategy_builder
        """
        close = data_parser.get_close(data)
        macd = indicators.macd(close)
        macd_series = macd['macd']
        macd_signal = macd['macdsignal']
        buy = Condition(data1=macd_series, data2=macd_signal, operation=Operation.CROSSOVER)
        sell = Condition(data1=macd_series, data2=macd_signal, operation=Operation.CROSSUNDER)
        chart_1 = ChartElement(data=macd, label="macd", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                               color=ChartColor.BLUE)
        charts = [chart_1]
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=BUY, buy=buy, sell=sell,
                                  charts=charts)
        show_back_testing_reports(result)
        return result

    @staticmethod
    def rsi(data: list, data_properties: dict) -> dict:
        """
        Strategy for Relative Strength Index.
        :param data: list[numeric]
        :param data_properties: dict
        :return: dict
                Result from strategy_builder
        """
        close = data_parser.get_close(data)
        rsi = indicators.rsi(close, period=5)
        buy = Condition(data1=rsi, data2=35, operation=Operation.LESS_THAN)
        # sell = Condition(data1=rsi, data2=80, operation=Operation.GREATER_THAN)
        sell_01 = Condition(data1=rsi, data2=28, operation=Operation.LESS_THAN)
        chart_1 = ChartElement(data=rsi, label="rsi", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS,
                               color=ChartColor.PINK)
        charts = [chart_1]
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=BUY, buy=buy, target=.5,
                                  sl=sell_01,
                                  charts=charts)
        show_back_testing_reports(result)
        return result

    @staticmethod
    def stoch(data: list, data_properties: dict) -> dict:
        """
        Strategy for Stochastic Oscillator.
        :param data: list[numeric]
        :param data_properties: dict
        :return: dict
                Result from strategy_builder
        """
        high = data_parser.get_high(data)
        low = data_parser.get_low(data)
        close = data_parser.get_close(data)
        stoch = indicators.stoch(high, low, close)
        fastk = stoch['fastk']
        fastd = stoch['fastd']
        buy = Condition(data1=fastk, data2=fastd, operation=Operation.CROSSOVER)
        sell = Condition(data1=fastk, data2=fastd, operation=Operation.CROSSUNDER)
        charts = [
            ChartElement(data=stoch, label="STOCH", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                         color="#85FF45")]
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=BUY, buy=buy, sell=sell,
                                  charts=charts)
        show_back_testing_reports(result)
        return result

    @staticmethod
    def bbands(data: list, data_properties: dict) -> dict:
        """
        Strategy for Bollinger Bands.
        :param data: list[numeric]
        :param data_properties: dict
        :return: dict
                Result from strategy_builder
        """
        close = data_parser.get_close(data)
        bbands = indicators.bollinger_bands(close, timeperiod=20)
        upperband = bbands['upperband']
        middleband = bbands['middleband']
        lowerband = bbands['lowerband']
        buy = Condition(data1=close, data2=middleband, operation=Operation.LESS_THAN)
        sell = Condition(data1=close, data2=middleband, operation=Operation.GREATER_THAN)
        chart_1 = ChartElement(data=bbands, label="bbands", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                               color="magenta")
        charts = [chart_1]
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=SELL, buy=buy, sell=sell,
                                  charts=charts, target=lowerband, sl=upperband)
        show_back_testing_reports(result)
        return result

    @staticmethod
    def pivot(data: list, data_properties: dict) -> dict:
        """
        Strategy for Pivot points.
        :param data: list[numeric]
        :param data_properties: dict
        :return: dict
                Result from strategy_builder
        """
        close = data_parser.get_close(data)
        pivot = indicators.pivot(data)
        pp = pivot['pp']
        r1 = pivot['r1']
        s1 = pivot['s1']
        buy = Condition(data1=close, data2=pp, operation=Operation.GREATER_THAN)
        sell = Condition(data1=close, data2=pp, operation=Operation.LESS_THAN)
        chart_1 = ChartElement(data=pivot, label="pivot", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                               color=ChartColor.GREEN)
        charts = [chart_1]
        data_properties.update({"chart": "Line"})
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=BUY, buy=buy, sell=sell,
                                  charts=charts, target=r1, sl=s1)
        show_back_testing_reports(result)
        return result


order_target = None
order_sl = None
pending_order = False
first_order = True


def strategy_builder(data_properties: dict, data_list: list, charts: list = None,
                     buy: Union[Condition, ConditionsLogic] = None,
                     sell: Union[Condition, ConditionsLogic] = None, target: Union[Condition, float] = None,
                     sl: Union[Condition, float] = None, strategy: str = BUY, qty: int = 1) -> dict:
    """
    It is used to build strategy based on different conditions.
    :param data_properties: dict
                Properties of the data given to the strategy.
    :param data_list: list
                list[DataObejct]
    :param charts: list
                list[ChartElement]
    :param buy: Union[Condition, ConditionsLogic]
                It can be a Condition, ConditionLogic or a list of Condition or ConditionLogic or both
    :param sell: Union[Condition, ConditionsLogic]
                It can be a Condition, ConditionLogic or a list of Condition or ConditionLogic or both
    :param target: Union[Condition, float]
                Target or profit condition.
                It can be a Condition, ConditionLogic or a list of Condition or ConditionLogic or both
                Value can also be given in numeric. This will be treated as percentage for target value.
    :param sl: Union[Condition, float]
                Stop loss or sl condition.
                It can be a Condition, ConditionLogic or a list of Condition or ConditionLogic or both
                Value can also be given in numeric. This will be treated as percentage for stop loss value
    :param strategy: str
                It can be either strategy.BUY or strategy.SELL
    :param qty: int
                Any positive int value
    :return: dict
                It returns a dict of the form
                dict(
                    data_properties=dict,
                    data=list,
                    params=list,
                    all=dict,
                    long=dict,
                    short=dict,
                    annotations=list
                )
    """
    global order_target, order_sl, pending_order, first_order
    order_target = None
    order_sl = None
    pending_order = False
    first_order = True
    data_prop, params, data = data_parser.data_builder(data_list, charts=charts, data_properties=data_properties)
    length = 0
    buy_condition, sell_condition = [], []

    if buy is not None:
        buy_condition = _evaluate_order_conditions(buy)
        length = len(buy_condition)
    if sell is not None:
        sell_condition = _evaluate_order_conditions(sell)
        length = len(sell_condition)
    if (buy is None) & (sell is None):
        _logger.warning("No condition in either buy or sell")
        _logger.warning("Exiting...")
        return dict()
    if buy is None:
        buy_condition = [False] * length
    if sell is None:
        sell_condition = [False] * length

    profit_condition = _check_book_conditions(target)
    sl_condition = _check_book_conditions(sl)

    bt_all_date, bt_all_signal, bt_all_qty, bt_all_price, bt_all_pl, bt_all_cum_pl = [], [], [], [], [], []
    bt_long_date, bt_long_signal, bt_long_qty, bt_long_price, bt_long_pl, bt_long_cum_pl = [], [], [], [], [], []
    bt_short_date, bt_short_signal, bt_short_qty, bt_short_price, bt_short_pl, bt_short_cum_pl = [], [], [], [], [], []
    bt_all_date_cum_pl, bt_long_date_cum_pl, bt_short_date_cum_pl = [], [], []
    annotations = []
    # Master index for data will be one ahead of the buy and sell conditions
    for i in range(length):
        buy_signal = buy_condition[i]
        sell_signal = sell_condition[i]
        date = data[i][0]
        # open = master[i][1]
        # high = master[i][2]
        low = data[i][3]
        close = data[i][4]

        def bt_add_order(signal):
            global pending_order, first_order
            if first_order:
                bt_all_pl.append(0)
                bt_all_cum_pl.append(0)
            else:
                if pending_order:
                    pl = (close - bt_all_price[-1]) * qty
                    cum_pl = bt_all_cum_pl[-1] + pl
                    bt_all_date_cum_pl.append([date, cum_pl])
                else:
                    pl = None
                    cum_pl = bt_all_cum_pl[-1]
                bt_all_pl.append(pl)
                bt_all_cum_pl.append(cum_pl)
            bt_all_date.append(date)
            bt_all_signal.append(signal)
            bt_all_qty.append(qty)
            bt_all_price.append(close)
            if signal.__contains__(BUY):
                _logger.debug("Long trade")
                if first_order:
                    bt_long_pl.append(0)
                    bt_long_cum_pl.append(0)
                    first_order = False
                else:
                    if pending_order:
                        pl = (close - bt_long_price[-1]) * qty
                        cum_pl = bt_long_cum_pl[-1] + pl
                        bt_long_date_cum_pl.append([date, cum_pl])
                    else:
                        pl = None
                        if len(bt_long_cum_pl) == 0:
                            bt_long_pl.append(0)
                            bt_long_cum_pl.append(0)
                        else:
                            cum_pl = bt_long_cum_pl[-1]
                    bt_long_pl.append(pl)
                    bt_long_cum_pl.append(cum_pl)
                bt_long_date.append(date)
                bt_long_signal.append(signal)
                bt_long_qty.append(qty)
                bt_long_price.append(close)
            if signal.__contains__(SELL):
                _logger.debug("Short Trade")
                if first_order:
                    bt_short_pl.append(0)
                    bt_short_cum_pl.append(0)
                    first_order = False
                else:
                    if pending_order:
                        pl = (close - bt_short_price[-1]) * qty
                        cum_pl = bt_short_cum_pl[-1] + pl
                        bt_short_date_cum_pl.append([date, cum_pl])
                    else:
                        pl = None
                        if len(bt_short_cum_pl) == 0:
                            bt_short_pl.append(0)
                            bt_short_cum_pl.append(0)
                        else:
                            cum_pl = bt_short_cum_pl[-1]
                    bt_short_pl.append(pl)
                    bt_short_cum_pl.append(cum_pl)
                bt_short_date.append(date)
                bt_short_signal.append(signal)
                bt_short_qty.append(qty)
                bt_short_price.append(close)
            if signal.__contains__(BUY):
                if signal.__contains__(TARGET):
                    annotations.append([date, low, "BP"])
                elif signal.__contains__(SL):
                    annotations.append([date, low, "BSL"])
                else:
                    annotations.append([date, low, "BR"])
            if signal.__contains__(SELL):
                if signal.__contains__(TARGET):
                    annotations.append([date, low, "SSP"])
                elif signal.__contains__(SL):
                    annotations.append([date, low, "SSL"])
                else:
                    annotations.append([date, low, "SR"])

        def buy_order():
            global order_target, order_sl, pending_order
            if (profit_condition is not None) & (type(profit_condition) == float):
                order_target = close + (close * profit_condition)
            if (sl_condition is not None) & (type(sl_condition) == float):
                order_sl = close - (close * sl_condition)
            _logger.debug("Date: %s Price: %s" % (date, close))
            _logger.debug("Placed a %s order with target %s and sl %s" % (BUY, order_target, order_sl))
            bt_add_order(signal=BUY)

        def sell_order():
            global order_target, order_sl, pending_order
            if (profit_condition is not None) & (type(profit_condition) == float):
                order_target = close - (close * profit_condition)
            if (sl_condition is not None) & (type(sl_condition) == float):
                order_sl = close + (close * sl_condition)
            _logger.debug("Date: %s Price: %s" % (date, close))
            _logger.debug("Placed a %s order with target %s and sl %s" % (SELL, order_target, order_sl))
            bt_add_order(signal=SELL)

        # If order is pending book profit or sl
        if pending_order:
            if (profit_condition is not None) & (type(profit_condition) == list):
                order_target = profit_condition[i]
            if (sl_condition is not None) & (type(sl_condition) == list):
                order_sl = sl_condition[i]

            if strategy == BUY:
                if (order_target is True) | (close >= order_target):
                    _logger.debug("Target hit on %s" % date)
                    bt_add_order(signal=TARGET + " in " + BUY)
                    pending_order = False
                elif (order_sl is True) | (close <= order_sl):
                    _logger.debug("SL hit on %s" % date)
                    bt_add_order(signal=SL + " in " + BUY)
                    pending_order = False

                if sell_signal:
                    if pending_order:
                        _logger.debug("Date: %s Price: %s" % (date, close))
                        _logger.debug(SELL)
                        bt_add_order(signal=SELL)
                        sell_order()
                    sell_order()
                    pending_order = True
                    strategy = SELL

            if strategy == SELL:
                if (order_target is True) | (close <= order_target):
                    _logger.debug("Target hit on %s" % date)
                    bt_add_order(signal=TARGET + " in " + SELL)
                    pending_order = False
                elif (order_sl is True) | (close >= order_sl):
                    _logger.debug("SL hit on %s" % date)
                    bt_add_order(signal=SL + " in " + SELL)
                    pending_order = False

                if buy_signal:
                    if pending_order:
                        _logger.debug("Date: %s Price: %s" % (date, close))
                        _logger.debug(BUY)
                        bt_add_order(signal=BUY)
                        pending_order = False
                    buy_order()
                    pending_order = True
                    strategy = BUY
        # If there is no pending order then place order according to the strategy
        else:
            if strategy == BUY:
                if buy_signal:
                    buy_order()
                    pending_order = True
            if strategy == SELL:
                if sell_signal:
                    sell_order()
                    pending_order = True

    bt_all = dict(
        Date=bt_all_date,
        Signal=bt_all_signal,
        QTY=bt_all_qty,
        Price=bt_all_price,
        P_L=bt_all_pl,
        CUM_P_L=bt_all_cum_pl,
        DATE_CUM_PL=bt_all_date_cum_pl
    )
    bt_long = dict(
        Date=bt_long_date,
        Signal=bt_long_signal,
        QTY=bt_long_qty,
        Price=bt_long_price,
        P_L=bt_long_pl,
        CUM_P_L=bt_long_cum_pl,
        DATE_CUM_PL=bt_long_date_cum_pl
    )
    bt_short = dict(
        Date=bt_short_date,
        Signal=bt_short_signal,
        QTY=bt_short_qty,
        Price=bt_short_price,
        P_L=bt_short_pl,
        CUM_P_L=bt_short_cum_pl,
        DATE_CUM_PL=bt_short_date_cum_pl
    )
    result = dict(
        data_properties=data_prop,
        data=data,
        params=params,
        all=bt_all,
        long=bt_long,
        short=bt_short,
        annotations=annotations
    )
    return result


def _evaluate_order_conditions(order) -> list:
    """
    Used for evaluating conditions.
    :param order: Any
    :return: list
    """
    result = []
    order_evaluator = []
    if type(order) == list:
        for item in order:
            if type(item) == Condition:
                order_evaluator.append(_calc_condition(item))
            elif type(item) == ConditionsLogic:
                order_evaluator.append(_calc_conditions_logic(item))
            else:
                _logger.warning("Incorrect condition in Order")
        if len(order_evaluator) == 1:
            result = (order_evaluator[0])
        elif len(order_evaluator) > 1:
            while len(order_evaluator) == 1:
                # noinspection PyTypeChecker
                order_evaluator[0] = _logic_evaluator(order_evaluator[0], order_evaluator[1], operation=auto_op)
                order_evaluator.pop(1)
            result = (order_evaluator[0])
    elif type(order) == Condition:
        result = (_calc_condition(order))
    elif type(order) == ConditionsLogic:
        result = (_calc_conditions_logic(order))
    else:
        _logger.warning("Incorrect condition in Order or no Condition specified")
    return result


def _calc_conditions_logic(cond_logic=ConditionsLogic):
    """
    Evaluates a ConditionLogic object.
    :param cond_logic: ConditionLogic
    :return: list
    """
    temp = []
    cond1 = cond_logic.cond1
    cond2 = cond_logic.cond2
    op = cond_logic.logic
    temp.append(_evaluate_logical_element(cond1))
    temp.append(_evaluate_logical_element(cond2))
    result = (_logic_evaluator(temp[0], temp[1], operation=op))
    # _logger.warning("Incorrect data type specified in ConditionLogic Object")
    return result


def _evaluate_logical_element(logic_element):
    """
    Used for evaluating different type of inputs
    :param logic_element: Any
    :return: Any
    """
    if type(logic_element) == Condition:
        return _calc_condition(logic_element)
    elif type(logic_element) == ConditionsLogic:
        return _calc_conditions_logic(logic_element)
    else:
        _logger.warning("Unable to evaluate condition in ConditionsLogic element")
        return None


def _logic_evaluator(arr1, arr2, operation=Logical):
    """
    Used for evaluating a logical operation between data list.
    :param arr1:
    :param arr2:
    :param operation:
    :return:
    """
    result = []
    exp = 'item1 %s item2' % operation
    for i in range(len(arr1)):
        data = {"item1": arr1[i], "item2": arr2[i]}
        result.append(eval(exp, data))
    return result


def _calc_condition(condition=Condition) -> list:
    """
    Used to evaluate a Condition Object
    :param condition: Condition
    :return: list
    """
    result = []
    offset = 0
    if condition.data2 is not None:
        if _check_number(condition.data2):
            condition.data2 = [condition.data2] * len(condition.data1)
    if len(condition.data1) != len(condition.data2):
        return result
    else:
        for i in range(len(condition.data1)):
            data_m = condition.data1[i]
            data_n = condition.data2[i]
            if condition.operation is not None:
                if _check_data(data_m) & _check_data(data_n):
                    if (condition.operation == Operation.CROSSOVER) | (condition.operation == Operation.CROSSUNDER):
                        if offset == 0:
                            offset = 1
                            result.append(False)
                        elif offset == 1:
                            data_m_1 = condition.data1[i - 1]
                            data_n_1 = condition.data2[i - 1]
                            if condition.operation == Operation.CROSSOVER:
                                result.append(
                                    _cross_over(data_m_1=data_m_1, data_n_1=data_n_1, data_m=data_m, data_n=data_n))
                            elif condition.operation == Operation.CROSSUNDER:
                                result.append(
                                    _cross_under(data_m_1=data_m_1, data_n_1=data_n_1, data_m=data_m, data_n=data_n))
                            else:
                                result.append(False)
                    elif condition.operation == Operation.RANGE_EQUAL:
                        result.append(_evaluate_range(data_m=data_m, data_n=data_n))
                    else:
                        result.append(_evaluate_op(data_m=data_m, data_n=data_n, operation=condition.operation))
                else:
                    result.append(False)
            else:
                _logger.warning("No operation specified in %s" % condition)
    return result


def _check_book_conditions(order):
    """
    Used for evaluating book conditions (profit, sl)
    :param order: Any
    :return: Any
    """
    if order is None:
        _logger.warning("No condition specified in profit/sl")
        return None
    elif _check_number(order):
        _logger.debug("Book value in percentage: %s" % order)
        return (float(order)) / 100.0
    elif type(order) == list:
        if _check_number(order[-1]):
            result = order
            return result
        else:
            _logger.debug("Book value not in percentage")
            result = _evaluate_order_conditions(order)
            return result
    else:
        _logger.debug("Book value not in percentage")
        result = _evaluate_order_conditions(order)
        return result


def _check_data(data):
    """
    Check whether data is nan or None
    :param data: data entry
    :return: Boolean
            True if data is valid(have a value)
            False if data is invalid
    """
    if (data == constants.default) | (data is None):
        return False
    else:
        return True


def _check_number(data):
    """
    Check whether data is numeric.
    :param data: Any
    :return: Boolean
    """
    if (type(data) == int) | (type(data) == float):
        return True
    else:
        return False


def _cross_over(data_m_1, data_m, data_n_1, data_n):
    """
    Used for evaluating Cross Over
    :param data_m_1: Previous candle data for data 1
    :param data_m: Current candle data for data 1
    :param data_n_1: Previous candle data for data 2
    :param data_n: Current candle data for data 2
    :return: Boolean
    """
    if (data_m_1 < data_n_1) & (data_m > data_n):
        return True
    else:
        return False


def _cross_under(data_m_1, data_m, data_n_1, data_n):
    """
    Used for evaluating Cross Under
    :param data_m_1: Previous candle data for data 1
    :param data_m: Current candle data for data 1
    :param data_n_1: Previous candle data for data 2
    :param data_n: Current candle data for data 2
    :return: Boolean
    """
    if (data_m_1 > data_n_1) & (data_m < data_n):
        return True
    else:
        return False


def _evaluate_range(data_m, data_n):
    """
    Used for evaluating range equal operation
    :param data_m: Current candle data for data 1
    :param data_n: Current candle data for data 2
    :return: Boolean
    """
    dev = 0.1
    if _check_number(data_n):
        exp = "(data_n - (data_n * dev)) <= data_m <= (data_n + (data_n * dev))"
        data = {"data_m": data_m, "data_n": data_n, "dev": dev}
        value = eval(exp, data)
        return value
    else:
        _logger.warning("Value for Range Equal operation is not a numeric value")
        return False


def _evaluate_op(data_m, data_n, operation):
    """
    Used for evaluating logical operation
    :param data_m: Current candle data for data 1
    :param data_n: Current candle data for data 2
    :param operation: Operation
    :return: Boolean
    """
    exp = "var1 %s var2" % operation
    data = {"var1": data_m, "var2": data_n}
    value = eval(exp, data)
    return value


def show_back_testing_reports(result: dict, auto_open: bool = True, strategy: str = ""):
    """
    Displays the back test reports in browser.
    :param result: dict returned by strategy_builder
    :param auto_open: Boolean
    :param strategy: str
            Name of the strategy
    :return: None
    """
    show_results(result['all'], auto_open, filename="reports/%s_all_trades.html" % strategy)
    show_results(result['long'], auto_open, filename="reports/%s_long_trades.html" % strategy)
    show_results(result['short'], auto_open, filename="reports/%s_short_trades.html" % strategy)


def show_results(result: dict, auto_open: bool, filename: str = 'result_table.html'):
    """
    Displays results in browser.
    :param result: dict
    :param auto_open: Boolean
    :param filename: Name for the file
    :return: None
    """
    keys = []
    values = []
    for key, value in result.items():
        keys.append(key)
        values.append(value)

    trace = go.Table(
        header=dict(values=keys,
                    line=dict(color='#7D7F80'),
                    fill=dict(color='#a1c3d1'),
                    align=['left'] * 5),
        cells=dict(values=values,
                   line=dict(color='#7D7F80'),
                   fill=dict(color='#EDFAFF'),
                   align=['left'] * 5))

    # layout = dict(width=700, height=700)
    data = [trace]
    # fig = dict(data=data, layout=layout)
    fig = dict(data=data)
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)
