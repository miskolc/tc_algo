import json

import requests

from algo import config_manager

login_url = "http://tradingcampus.net:17007/api/PublicAPI/LoginRequest"
order_url = "http://tradingcampus.net:17007/api/PublicAPI/OrderEntry"
order_status_url = "http://tradingcampus.net:17007/api/PublicAPI/OrderStatusRequest"
modify_order_url = "http://tradingcampus.net:17007/api/PublicAPI/ModifyRequest"
cancel_order_url = "http://tradingcampus.net:17007/api/PublicAPI/CancelRequest"
trade_book_url = "http://tradingcampus.net:17007/api/PublicAPI/TradeBookRequest"
position_book_url = "http://tradingcampus.net:17007/api/PublicAPI/PositionRequest"
order_book_url = "http://tradingcampus.net:17007/api/PublicAPI/OrderBookRequest"


def login_request():
    login_id, password = config_manager.get_credentials()
    data = dict(LoginId=login_id, Password=password)
    status = requests.post(login_url, json=data)
    response = json.loads(status.content)
    print(response['UniqueId'], response['RefNo'])


# Requires Modification
def place_order():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(order_url, json=data)
    response = json.loads(status.content)
    print(response)


# Requires Modification
def order_status():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(order_status_url, json=data)
    response = json.loads(status.content)
    print(response)


# Requires Modification
def modify_order():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(modify_order_url, json=data)
    response = json.loads(status.content)
    print(response)


# Requires Modification
def cancel_order():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(cancel_order_url, json=data)
    response = json.loads(status.content)
    print(response)


# Requires Checking
def trade_book_request():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(trade_book_url, json=data)
    response = json.loads(status.content)
    print(response)


# Requires Checking
def position_book_request():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(position_book_url, json=data)
    response = json.loads(status.content)
    print(response)


# Requires Checking
def order_book_request():
    unique_id, ref_no = config_manager.get_api_credentials()
    data = dict(UniqueId=unique_id, RefNo=ref_no)
    status = requests.post(order_book_url, json=data)
    response = json.loads(status.content)
    print(response)


if __name__ == '__main__':
    # login_request()
    place_order()
