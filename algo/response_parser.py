import logging
from pprint import pprint

from algo import config_manager
from constants import ApiKeys as k

_logger = logging.getLogger("api_reader")


def read_login_response(response):
    unique_id = response[k.unique_id]
    ref_no = response[k.ref_no]
    error = response[k.error]
    if error is None:
        _logger.info("Login Success")
        config_manager.set_api_credentials(unique_id, ref_no)
        _logger.info("API credentials updated")
    else:
        _logger.warning("Error while Login attempt")
        _logger.info("Error: %s" % error)


def read_order_response(response):
    order_no = response[k.order_no]
    error = response[k.error]
    if error is None:
        _logger.info("Order placed successfully")
        _logger.info("Order No: %s" % order_no)
    else:
        _logger.warning("Error while Placing the order")
        _logger.info("Error: %s" % error)


def read_order_status_response(order_id, response):
    _logger.info("Response for order no: %s ---> %s" % (order_id, response))


def read_order_cancel_response(response):
    order_no = response[k.order_no]
    error = response[k.error]
    if error is None:
        _logger.info("Order Cancelled successfully")
        _logger.info("Order No: %s" % order_no)
    else:
        _logger.warning("Error while cancelling the order")
        _logger.info("Error: %s" % error)


def read_order_modify_response(response):
    order_no = response[k.order_no]
    error = response[k.error]
    if error is None:
        _logger.info("Order Modified Successfully")
        _logger.debug("Order No: %s" % order_no)
    else:
        _logger.warning("Error while modifying the order")
        _logger.info("Error: %s" % error)


def read_trade_book_response(response):
    if len(response) > 0:
        pprint(response)
    else:
        _logger.info("Nothing in Trade book")


def read_position_book_response(response):
    if len(response) > 0:
        pprint(response)
    else:
        _logger.info("Nothing in Position book")


def read_order_book_response(response):
    if len(response) > 0:
        pprint(response)
    else:
        _logger.info("Nothing in Order book")
