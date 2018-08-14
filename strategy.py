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


def strategy_builder(data=list, indicator=dict, buy=Condition, sell=Condition, strategy=str):
    master = data_parser.data_builder(data, **indicator)
    buy_condition = _evaluate_order_conditions(buy)
    sell_condition = _evaluate_order_conditions(sell)


def _evaluate_order_conditions(order) -> list:
    result = []
    order_evaluator = []
    if type(order) == list:
        for item in order:
            if type(item) == Condition:
                order_evaluator.append(_condition_evaluator(item))
            elif type(item) == ConditionsLogic:
                order_evaluator.append(_evaluate_conditions_logic(item))
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
        result = (_condition_evaluator(order))
    elif type(order) == ConditionsLogic:
        result = (_evaluate_conditions_logic(order))
    else:
        _logger.warning("Incorrect condition in Order or no Condition specified")
    return result


def _evaluate_conditions_logic(cond_logic=ConditionsLogic):
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
        return _condition_evaluator(logic_element)
    elif type(logic_element) == ConditionsLogic:
        return _evaluate_conditions_logic(logic_element)
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


def _condition_evaluator(condition=Condition) -> list:
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
