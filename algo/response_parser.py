import logging

from algo import config_manager
from constants import ApiKeys as k

_logger = logging.getLogger("api_reader")


def read_login_response(response):
    unique_id = response[k.unique_id]
    ref_no = response[k.ref_no]
    error = response[k.error]
    if ref_no is not None:
        _logger.info("Login Success")
        config_manager.set_api_credentials(unique_id, ref_no)
        _logger.info("API credentials updated")
    else:
        _logger.warning("Error while Login attempt")
        _logger.info("Error: %s" % error)


def read_order_response(response):
    pass


def read_order_cancel_response(response):
    pass


def read_order_modify_response(response):
    pass


def read_trade_book_response(response):
    pass


def read_position_book_response(response):
    pass


def read_order_book_response(response):
    pass
