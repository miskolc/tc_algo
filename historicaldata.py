import json

import requests
from model import Scrip, ct

scrip = Scrip(symbol="NIFTY 50", exchange="NSECM", gateway_id=2, token_no=0, instrument="INDEX", symbol_desc="NIFTY 50",
              lot_size=75, isin_number="", series="EQ", strike_price=0.0)


def get_historical_data(login_id: str, gateway: ct.Gateway = ct.Gateway.NSECM, symbol: Scrip = scrip,
                        start_time: str = "01/01/2018 9:15am", end_time: str = "07/09/2018 3:15pm", minute: int = 5):
    # defining the api-endpoint
    API_ENDPOINT = "http://115.112.230.27:8004/api/TCService/GetDateWiseSymbolData"

    # data to be sent to api
    data = {
        "LoginId": login_id,
        "GatewayId": gateway.name,
        "Exchange": gateway.name,
        "Symbol": symbol.symbol,
        "StartTime": start_time,
        "EndTime": end_time,
        "minute": "%s" % minute
    }
    # sending post request and saving response as Response object
    r = requests.post(url=API_ENDPOINT, data=data)
    # extracting response text
    content = r.content

    print("The content is:%s" % content)


def get_date_wise_symbol_data(login_id: str, gateway: ct.Gateway = ct.Gateway.NSECM, symbol: Scrip = scrip,
                              start_time: str = "01/01/2018 9:15am", end_time: str = "07/09/2018 3:15pm",
                              minute: int = 5):
    API_ENDPOINT = "http://115.112.230.26:8006/Service1.svc"
    method = "/GetDateWiseSymbolData"
    data = {
        "LoginId": login_id,
        "GatewayId": gateway.name,
        "Exchange": gateway.name,
        "Symbol": symbol.symbol,
        "StartTime": start_time,
        "EndTime": end_time,
        "minute": "%s" % minute
    }
    r = requests.post(url=API_ENDPOINT + method, data=json.dumps(data))
    content = r.content
    print(content)


# get_historical_data("SUJIT")
get_date_wise_symbol_data("SUJIT")
