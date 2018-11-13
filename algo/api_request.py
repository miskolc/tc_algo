import json
import logging
from pprint import pprint

import requests

from algo import config_manager, response_parser as reader
from constants import ApiKeys as k, OrderKeys as o
from contracts import NSECM
from model import Scrip

_logger = logging.getLogger("rest_api")
base_url = "http://tradingcampus.net:17007/api/PublicAPI/"
login_func = "LoginRequest"
order_func = "OrderEntry"
order_status_func = "OrderStatusRequest"
modify_order_func = "ModifyRequest"
cancel_order_func = "CancelRequest"
trade_book_func = "TradeBookRequest"
position_book_func = "PositionRequest"
order_book_func = "OrderBookRequest"


def send_request(func: str, data: dict):
    try:
        status = requests.post(base_url + func, json=data)
        response = json.loads(status.content)
        return response
    except (requests.ConnectionError, requests.HTTPError) as e:
        _logger.warning("Error while sending the request")
        _logger.info("Error: %s" % e)
        return


def login_request():
    login_id, password = config_manager.get_credentials()
    data = {k.key_login_id: login_id, k.key_password: password}
    response = send_request(login_func, data)
    reader.read_login_response(response)


def place_order(scrip: Scrip, buy_sell: str, qty: int, order_type: str, validity: str, price: float = None,
                trigger_price: float = None):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    login_id, password = config_manager.get_credentials()
    data = {k.unique_id: unique_id, k.key_login_id: login_id, k.ref_no: ref_no}
    if scrip:
        data.update({k.gateway: scrip.exchange, k.exchange: scrip.exchange, k.token_no: scrip.token_no})
        data.update({k.client_code: login_id})
        data.update({k.buy_sell: buy_sell}) if buy_sell in [o.BUY, o.SELL] else _logger.debug(
            "Incorrect value for parameter: buy_sell")
        data.update({k.qty: qty}) if int(qty) else _logger.debug("parameter qty can only be of type int")
        data.update({k.price: price}) if price else _logger.debug("Not a limit order")
        if order_type in [o.RL, o.SL]:
            if order_type == o.SL:
                if trigger_price is not None:
                    data.update({k.trigger_price: trigger_price, k.book_type: order_type})
                else:
                    _logger.warning("Trigger price is required for SL order")
            if order_type == o.RL:
                data.update({k.book_type: order_type})
        data.update({k.validity: validity})
    response = send_request(order_func, data)
    reader.read_order_response(response)


def order_status(order_id: int):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    data = {k.unique_id: unique_id, k.ref_no: ref_no, k.order_no: order_id}
    response = send_request(order_status_func, data)
    reader.read_order_status_response(order_id, response)


# {
#     "UniqueId": 97,
#     "RefNo": "gCgz2mRI1kiYLrnRbq1JQ6rGoJgCNlT1",
#     "IntOrdNo": 2,
#     "qty": 1000,
#     "price": 0,
#     "Booktype": "RL",
#     "validity": "DAY"
# }
def modify_order(order_id: int, price: float, qty: int, validity: str, order_type, trigger_price: float = None, ):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    data = {k.unique_id: unique_id, k.ref_no: ref_no, k.order_no: order_id}
    data.update({k.price: price, k.qty: qty})
    if order_type in [o.RL, o.SL]:
        if order_type == o.SL:
            if trigger_price is not None:
                data.update({k.trigger_price: trigger_price, k.book_type: order_type})
            else:
                _logger.warning("Trigger price is required for SL order")
        if order_type == o.RL:
            data.update({k.book_type: order_type})
    data.update({k.validity: validity})
    response = send_request(modify_order_func, data)
    # print(response)
    reader.read_order_modify_response(response)


def cancel_order(order_id: int):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    data = {k.unique_id: unique_id, k.ref_no: ref_no, k.order_no: order_id}
    response = send_request(cancel_order_func, data)
    reader.read_order_cancel_response(response)


def trade_book_request(order_id: int = None, scrip: Scrip = None):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    data = {k.unique_id: unique_id, k.ref_no: ref_no}
    if order_id:
        data.update({k.order_no: order_id})
    if scrip:
        data.update({k.token_no: scrip.token_no})
    response = send_request(trade_book_func, data)
    reader.read_trade_book_response(response)


def position_book_request(scrip: Scrip = None):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    data = {k.unique_id: unique_id, k.ref_no: ref_no}
    if scrip:
        data.update({k.token_no: scrip.token_no})
    response = send_request(position_book_func, data)
    reader.read_position_book_response(response)


def order_book_request(order_id: int = None, scrip: Scrip = None):
    unique_id, ref_no, modified = config_manager.get_api_credentials()
    data = {k.unique_id: unique_id, k.ref_no: ref_no}
    if order_id:
        data.update({k.order_no: order_id})
    if scrip:
        data.update({k.token_no: scrip.token_no})
    response = send_request(order_book_func, data)
    reader.read_order_book_response(response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # login_request()
    # place_order(NSECM._HDFCBANK_1333, o.BUY, 10, o.SL, o.DAY, price=1800, trigger_price=1750)
    # modify_order(3, 1800, 50, o.DAY, o.RL)
    # order_status(5)
    # cancel_order(4)
    # trade_book_request(order_id=5, scrip=NSECM._HDFCBANK_1333)
    # position_book_request(scrip=NSECM._HDFCAMC_4244)
    # order_book_request(scrip=NSECM._HDFCAMC_4244)
