# TODO: Operation for building conditions and Logical for logic with conditions
# TODO: Create a Condition function with params: HistoryData, indicator1, indicator2, operation/operator
# TODO: If the operation results in success then place a [Date,True] value
# TODO: For any reference contact or see cond.js
import logging

import data_parser
import indicators
from model import *

_logger = logging.getLogger("strategy")
BUY = "buy"
SELL = "sell"
auto_op = Logical.AND


def strategy_builder(data_list=list, indicator=dict, buy=Condition, sell=Condition, profit=None,
                     sl=None, strategy=str):
    # noinspection PyArgumentList
    master = data_parser.data_builder(data_list, **indicator)
    buy_condition = _evaluate_order_conditions(buy)
    sell_condition = _evaluate_order_conditions(sell)

    profit_condition = _check_book_conditions(profit)
    sl_condition = _check_book_conditions(sl)
    target = None
    sl = None
    pending_order = False

    # Master index for data will be one ahead of the buy and sell conditions
    for i in range(len(buy_condition)):
        buy_signal = buy_condition[i]
        sell_signal = sell_condition[i]
        date = master[i + 1][0]
        # open = master[i + 1][1]
        # high = master[i + 1][2]
        # low = master[i + 1][3]
        close = master[i + 1][4]
        # If order is pending book profit or sl
        if pending_order:
            if (profit_condition is not None) & (type(profit_condition) == list):
                target = profit_condition[i]
            if (sl_condition is not None) & (type(sl_condition) == list):
                sl = sl_condition[i]
            if strategy == BUY:
                if close == target:
                    _logger.info("Target hit on %s" % date)
                    pending_order = False
                elif close == sl:
                    _logger.info("SL hit on %s" % date)
                    pending_order = False
                elif sell_signal is True:
                    _logger.info("Date: %s Price: %s" % (date, close))
                    _logger.info(SELL)
                    pending_order = False

                    if (profit_condition is not None) & (type(profit_condition) == float):
                        order_target = close - close * profit_condition
                        target = order_target
                    if (sl_condition is not None) & (type(sl_condition) == float):
                        order_sl = close + close * sl_condition
                        sl = order_sl
                    _logger.info("Date: %s Price: %s" % (date, close))
                    _logger.info("Placed a %s order with target %s and sl %s" % (SELL, order_target, order_sl))
                    pending_order = True

            if strategy == SELL:
                if buy_signal is True:
                    if close == target:
                        _logger.info("Target hit on %s" % date)
                        pending_order = False
                    elif close == sl:
                        _logger.info("SL hit on %s" % date)
                        pending_order = False
                    elif sell_signal is True:
                        _logger.info("Date: %s Price: %s" % (date, close))
                        _logger.info(BUY)
                        pending_order = False

                        if (profit_condition is not None) & (type(profit_condition) == float):
                            order_target = close + close * profit_condition
                            target = order_target
                        if (sl_condition is not None) & (type(sl_condition) == float):
                            order_sl = close - close * sl_condition
                            sl = order_sl
                        _logger.info("Date: %s Price: %s" % (date, close))
                        _logger.info("Placed a %s order with target %s and sl %s" % (BUY, order_target, order_sl))
                        pending_order = True

        # If there is no pending order then place order according to the strategy
        else:
            order_target = None
            order_sl = None
            if strategy == BUY:
                if buy_signal is True:
                    if (profit_condition is not None) & (type(profit_condition) == float):
                        order_target = close + close * profit_condition
                        target = order_target
                    if (sl_condition is not None) & (type(sl_condition) == float):
                        order_sl = close - close * sl_condition
                        sl = order_sl
                    _logger.info("Date: %s Price: %s" % (date, close))
                    _logger.info("Placed a %s order with target %s and sl %s" % (BUY, order_target, order_sl))
                    pending_order = True
            if strategy == SELL:
                if sell_signal is True:
                    if (profit_condition is not None) & (type(profit_condition) == float):
                        order_target = close - close * profit_condition
                        target = order_target
                    if (sl_condition is not None) & (type(sl_condition) == float):
                        order_sl = close + close * sl_condition
                        sl = order_sl
                    _logger.info("Date: %s Price: %s" % (date, close))
                    _logger.info("Placed a %s order with target %s and sl %s" % (SELL, order_target, order_sl))
                    pending_order = True


def _evaluate_order_conditions(order) -> list:
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
    if type(logic_element) == Condition:
        return _calc_condition(logic_element)
    elif type(logic_element) == ConditionsLogic:
        return _calc_conditions_logic(logic_element)
    else:
        _logger.warning("Unable to evaluate condition in ConditionsLogic element")
        return None


def _logic_evaluator(arr1, arr2, operation=Logical):
    result = []
    exp = 'item1 %s item2' % operation
    for i in range(len(arr1)):
        data = {"item1": arr1[i], "item2": arr2[i]}
        result.append(eval(exp, data))
    return result


def _calc_condition(condition=Condition) -> list:
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
    if order is None:
        _logger.warning("No condition specified in profit/sl")
        return None
    elif _check_number(order):
        _logger.debug("Book value in percentage: %s" % order)
        return (float(order)) / 100.0
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
    if (data == indicators.default) | (data is None):
        return False
    else:
        return True


def _check_number(data):
    if (type(data) == int) | (type(data) == float):
        return True
    else:
        return False


def _cross_over(data_m_1, data_m, data_n_1, data_n):
    if (data_m_1 < data_n_1) & (data_m > data_n):
        return True
    else:
        return False


def _cross_under(data_m_1, data_m, data_n_1, data_n):
    if (data_m_1 > data_n_1) & (data_m < data_n):
        return True
    else:
        return False


def _evaluate_range(data_m, data_n):
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
    exp = "var1 %s var2" % operation
    data = {"var1": data_m, "var2": data_n}
    value = eval(exp, data)
    return value
