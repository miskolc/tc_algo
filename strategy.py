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


def strategy_builder(data=list, buy=list, sell=list, strategy=str, **kwargs):
    master = data_parser.data_builder(data, **kwargs)
    init_order = strategy
    pending_order = False
    buy_condition = []
    sell_condition = []
    profit, sl = [], []

    buy_signals = _evaluate_conditions(buy_condition)
    sell_signals = _evaluate_conditions(sell_condition)


def _evaluate_order_conditions(order) -> list:
    result = []
    if type(order) == Condition:
        order_condition = [order]
    elif type(order) == ConditionsLogic:
        order_condition = _evaluate_conditions_logic(order)
    elif type(order) == list:
        order_condition = order
    else:
        _logger.warning("Incorrect condition in Order")
    return result


def _evaluate_conditions_logic(order):
    result = []
    return result


def _evaluate_conditions(conditions=list):
    result = []
    cond_values = []
    for item in conditions:
        cond_values.append(_condition_evaluator(item))
    print(len(cond_values))
    return result


def _condition_evaluator(condition=Condition):
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
