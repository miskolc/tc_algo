import logging
from typing import List

import plotly.plotly
import plotly.graph_objs as go

import data_parser
import indicators
import pattern_hunter
from model import *

_logger = logging.getLogger("strategy")
BUY = "buy"
SELL = "sell"
TARGET = "target"
SL = "sl"
auto_op = Logical.AND
data_objects = []


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
                SMA = 0 (Default case)
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
        macd_series = macd[Keys.macd_value]
        macd_signal = macd[Keys.macdsignal]
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
        fastk = stoch[Keys.fastk]
        fastd = stoch[Keys.fastd]
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
        upperband = bbands[Keys.upperband]
        middleband = bbands[Keys.middleband]
        lowerband = bbands[Keys.lowerband]
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
        pp = pivot[Keys.pp]
        r1 = pivot[Keys.r1]
        s1 = pivot[Keys.s1]
        buy = Condition(data1=close, data2=pp, operation=Operation.GREATER_THAN)
        sell = Condition(data1=close, data2=pp, operation=Operation.LESS_THAN)
        chart_1 = ChartElement(data=pivot, label="pivot", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                               color=ChartColor.GREEN)
        charts = [chart_1]
        result = strategy_builder(data_properties=data_properties, data_list=data, strategy=BUY, buy=buy, sell=sell,
                                  charts=charts, target=r1, sl=s1, backtest_chart=ChartType.COLUMN)
        show_back_testing_reports(result)
        return result


order_target = None
order_sl = None
pending_order = False
first_order = True


def strategy_builder(data_properties: dict, data_list: list, charts: list = None,
                     buy: Union[Condition, ConditionsLogic, List[Condition], List[ConditionsLogic]] = None,
                     sell: Union[Condition, ConditionsLogic, List[Condition], List[ConditionsLogic]] = None,
                     target: Union[float, Condition, list] = None,
                     sl: Union[float, Condition, list] = None,
                     strategy: str = BUY,
                     qty: int = 1,
                     backtest_chart: ChartType = ChartType.LINE) -> dict:
    """
    It is used to build strategy based on different conditions.
    :param data_properties: dict
                Properties of the data given to the strategy.
    :param data_list: list
                list[DataObject]
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
    :param backtest_chart: ChartType
                Type of chart to be plotted for back testing results. By default: ChartType.LINE
                It can be only of two types ChartType.LINE or ChartType.COLUMN
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
    global order_target, order_sl, pending_order, first_order, data_objects
    data_objects = data_list
    order_target = None
    order_sl = None
    pending_order = False
    first_order = True
    data_prop, params, data = data_parser.data_builder(data_list, charts=charts, data_properties=data_properties)
    if (backtest_chart == ChartType.LINE) | (backtest_chart == ChartType.COLUMN):
        data_prop.update({Keys.bt_chart: backtest_chart.value})
    else:
        _logger.warning("Back testing chart only be line or column")
        data_prop.update({Keys.bt_chart: ChartType.LINE})
    length = 0
    buy_condition, sell_condition = [], []
    qty = qty * data_prop[Keys.size]
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
            global pending_order
            if len(bt_all_cum_pl) == 0:
                bt_all_pl.append(0)
                bt_all_cum_pl.append(0)
            else:
                if pending_order:
                    pl = data_parser.round_float((close - bt_all_price[-1]) * qty)
                    cum_pl = data_parser.round_float(bt_all_cum_pl[-1] + pl)
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
                if len(bt_long_cum_pl) == 0:
                    bt_long_pl.append(0)
                    bt_long_cum_pl.append(0)
                else:
                    if pending_order:
                        pl = data_parser.round_float((close - bt_long_price[-1]) * qty)
                        cum_pl = data_parser.round_float(bt_long_cum_pl[-1] + pl)
                        bt_long_date_cum_pl.append([date, cum_pl])
                    else:
                        pl = None
                        cum_pl = bt_long_cum_pl[-1]
                    bt_long_pl.append(pl)
                    bt_long_cum_pl.append(cum_pl)
                bt_long_date.append(date)
                bt_long_signal.append(signal)
                bt_long_qty.append(qty)
                bt_long_price.append(close)
            if signal.__contains__(SELL):
                _logger.debug("Short Trade")
                if len(bt_short_cum_pl) == 0:
                    bt_short_pl.append(0)
                    bt_short_cum_pl.append(0)
                else:
                    if pending_order:
                        pl = data_parser.round_float((close - bt_short_price[-1]) * qty)
                        cum_pl = data_parser.round_float(bt_short_cum_pl[-1] + pl)
                        bt_short_date_cum_pl.append([date, cum_pl])
                    else:
                        pl = None
                        cum_pl = bt_short_cum_pl[-1]
                    bt_short_pl.append(pl)
                    bt_short_cum_pl.append(cum_pl)
                bt_short_date.append(date)
                bt_short_signal.append(signal)
                bt_short_qty.append(qty)
                bt_short_price.append(close)
            if signal.__contains__(BUY):
                if signal.__contains__(TARGET):
                    annotations.append([date, low, Keys.buy_book_profit])
                elif signal.__contains__(SL):
                    annotations.append([date, low, Keys.buy_book_sl])
                else:
                    annotations.append([date, low, Keys.buy_regular])
            if signal.__contains__(SELL):
                if signal.__contains__(TARGET):
                    annotations.append([date, low, Keys.sell_book_profit])
                elif signal.__contains__(SL):
                    annotations.append([date, low, Keys.sell_book_sl])
                else:
                    annotations.append([date, low, Keys.sell_regular])

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

    bt_all = {
        Keys.date: bt_all_date,
        Keys.signal: bt_all_signal,
        Keys.quantity: bt_all_qty,
        Keys.price: bt_all_price,
        Keys.pl: bt_all_pl,
        Keys.cum_pl: bt_all_cum_pl,
        Keys.date_cum_pl: bt_all_date_cum_pl
    }

    bt_long = {
        Keys.date: bt_long_date,
        Keys.signal: bt_long_signal,
        Keys.quantity: bt_long_qty,
        Keys.price: bt_long_price,
        Keys.pl: bt_long_pl,
        Keys.cum_pl: bt_long_cum_pl,
        Keys.date_cum_pl: bt_long_date_cum_pl
    }
    bt_short = {
        Keys.date: bt_short_date,
        Keys.signal: bt_short_signal,
        Keys.quantity: bt_short_qty,
        Keys.price: bt_short_price,
        Keys.pl: bt_short_pl,
        Keys.cum_pl: bt_short_cum_pl,
        Keys.date_cum_pl: bt_short_date_cum_pl
    }
    result = {
        Keys.data_prop: data_prop,
        Keys.data: data,
        Keys.params: params,
        Keys.all: bt_all,
        Keys.long: bt_long,
        Keys.short: bt_short,
        Keys.annotations: annotations
    }
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


def _logic_evaluator(arr1, arr2, operation: Logical):
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
    if type(condition.data1) == Pattern:
        if (condition.operation == Operation.BULL_RANGE) | (condition.operation == Operation.BEAR_RANGE):
            open, high, low, close = data_parser.get_ohlc(data_objects)
            result = _evaluate_patterns(open, high, low, close, pattern=condition.data1,
                                        pattern_range=condition.operation.value)
            return result
        else:
            _logger.warning("Operation for pattern can be either a BULL_RANGE or BEAR_RANGE")
    else:
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
                                    result.append(_cross_under(data_m_1=data_m_1, data_n_1=data_n_1, data_m=data_m,
                                                               data_n=data_n))
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
    if (data == ct.default) | (data is None):
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

    if result.__contains__("DATE_CUM_PL"):
        result.pop("DATE_CUM_PL")

    for key, value in result.items():
        keys.append(key)
        values.append(value)

    trace = go.Table(
        header=dict(values=keys,
                    line=dict(color='#7D7F80'),
                    fill=dict(color='#a1c3d1'),
                    align=['center'] * 5),
        cells=dict(values=values,
                   line=dict(color='#7D7F80'),
                   fill=dict(color='#EDFAFF'),
                   align=['left'] * 5))

    data = [trace]
    fig = dict(data=data)
    plotly.offline.plot(fig, filename=filename, auto_open=auto_open)


def _evaluate_patterns(open: list, high: list, low: list, close: list, pattern: Union[Pattern, list],
                       pattern_range: list) -> list:
    """

    :param open: list
                list[numeric]
    :param high: list
                list[numeric]
    :param low: list
                list[numeric]
    :param close: list
                list[numeric]
    :param pattern: Union[Pattern, list]
                Pattern or Patterns to be analysed along with the strategy. If a pattern is bullish and
                Strategy is BUY then we will give a signal for a buy and similarly for SELL strategy and
                bearish pattern sell signal will be generated.
    :param pattern_range: list
                This parameter needs to be specified if patterns are used in the strategy. For e.g. [50,100]
                A range of values which should appear in the strategy for the pattern(s) specified.
                If more than two values are mentioned then max and min will be taken and others will be discarded.
                A pattern value may range from -100 to +100.
                Values for each pattern is specified and accordingly their importance.
    :return: list[Boolean]
    """
    pattern_values, result = [], []
    max_range, min_range = 0, 0
    if type(pattern_range) == list:
        max_range = max(pattern_range)
        min_range = min(pattern_range)
    if type(pattern) == Pattern:
        x = pattern_hunter.pattern_hunter(open, high, low, close, pattern)
        pattern_values.append(x)
    elif type(pattern) == list:
        for item in pattern:
            if type(item) == Pattern:
                y = pattern_hunter.pattern_hunter(open, high, low, close, item)
                pattern_values.append(y)
            else:
                _logger.warning("Expected a type of %s got %s instead" % (Pattern, item))
    else:
        _logger.debug("Invalid input in patterns for strategy_builder")
        _logger.warning("Expected a type of %s got %s instead" % (Pattern, type(pattern)))

    def add_as_list(data_arr):
        res = []
        for j in range(len(data_arr)):
            res.append([data_arr[j]])
        return res

    pattern_arr = []
    if len(pattern_values) == 1:
        pattern_arr = add_as_list(pattern_values[0])
    elif len(pattern_values) > 1:
        father = add_as_list(pattern_values[0])
        pattern_values.pop(0)
        for arr in pattern_values:
            for i in range(len(arr)):
                father[i] = father[i] + [arr[i]]
            pattern_arr = father

    for k in range(len(pattern_arr)):
        val = False
        for m in pattern_arr[k]:
            if min_range <= m <= max_range:
                val = True
        result.append(val)
    return result


# noinspection PyTypeChecker
def strategy_optimizations(data_properties: dict, data_list: list, charts: list = None,
                           buy: Union[Condition, ConditionsLogic, List[Condition], List[ConditionsLogic]] = None,
                           sell: Union[Condition, ConditionsLogic, List[Condition], List[ConditionsLogic]] = None,
                           strategy: str = BUY,
                           qty: int = 1,
                           backtest_chart: ChartType = ChartType.LINE,
                           target_range: Union[list, numpy.ndarray, float] = None,
                           sl_range: Union[list, numpy.ndarray, float] = None):
    _logger1 = logging.getLogger("strategy.optimizer")
    length = 0
    if (type(target_range) != float) & (type(sl_range) != float):
        if type(target_range) == list:
            length = len(target_range)
        if type(sl_range) == list:
            length = len(sl_range)
        if type(target_range) == numpy.ndarray:
            target_range = target_range.tolist()
            length = len(target_range)
        if type(sl_range) == numpy.ndarray:
            sl_range = sl_range.tolist()
            length = len(sl_range)

        if (type(target_range) == float) | (type(sl_range) == float):
            if length > 0:
                if type(target_range) == float:
                    target_range = [target_range] * length
                elif type(sl_range) == float:
                    sl_range = [sl_range] * length

        if (type(target_range) == list) & (type(sl_range) == list):
            if len(target_range) == len(sl_range):
                heads = ["target", "sl", "p&l"]
                target, sl, cum_pl = [], [], []
                for i in range(len(target_range)):
                    _logger1.debug("For target: %s" % target_range[i])
                    _logger1.debug("For sl: %s" % sl_range[i])
                    result = strategy_builder(data_properties=data_properties, data_list=data_list, charts=charts,
                                              buy=buy,
                                              sell=sell, target=float(target_range[i]), sl=float(sl_range[i]),
                                              strategy=strategy, qty=qty, backtest_chart=backtest_chart)
                    target.append(target_range[i])
                    sl.append(sl_range[i])
                    cum_pl.append(result[Keys.all][Keys.cum_pl][-1])
                values = [target, sl, cum_pl]
                trace = go.Table(
                    header=dict(values=heads,
                                line=dict(color='#7D7F80'),
                                fill=dict(color='#a1c3d1'),
                                align=['center'] * 5),
                    cells=dict(values=values,
                               line=dict(color='#7D7F80'),
                               fill=dict(color='#EDFAFF'),
                               align=['left'] * 5))

                data = [trace]
                fig = dict(data=data)
                plotly.offline.plot(fig, filename="reports/optimize.html")
            else:
                _logger1.debug("Length differs for target and sl")
                _logger1.info("Target Length: %s" % len(target_range))
                _logger1.info("SL Length: %s" % len(sl_range))
        else:
            _logger1.debug("The type for both target and sl should be %s" % list)
    else:
        _logger1.warning("Both values can't be float")
