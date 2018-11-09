import json

import requests

login_url = "http://tradingcampus.net:17007/api/PublicAPI/LoginRequest"


def login_request():
    data = dict(LoginId="8288024014", Password="a@8888888888")
    status = requests.post(login_url, json=data)
    response = json.loads(status.content)
    print(response)


if __name__ == '__main__':
    login_request()
