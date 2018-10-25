# import time
# # import urllib
# from urllib import request
# from datetime import date
# import pandas as pd
#
# from options import database_connection as dbc
#
# columns = ['id', 'instrument', 'symbol', 'expiry', 'strike', 'option_typ', 'open', 'high', 'low', 'close', 'settle_pr',
#            'contracts', 'val', 'open_int', 'chg_in_oi', 'timestamp', 'iv', 'theta', 'gamma', 'delta', 'vega']
#
#
# def symbol_data(symbol, obs_date: str, expiry_date: str):
#     # call_query = "Select close, iv, delta, gamma, vega, theta from %s where symbol='%s' and instrument like 'OPT%%' " % (
#     call_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' " % (dbc.table_name, symbol,)
#     # print(call_query)
#     call_data = dbc.execute_simple_query(call_query)
#     # print(call_data)
#     return call_data
#
#
# def data_filter():
#     start_time = time.time()
#     data = symbol_data("NIFTY", "2018-10-22", "2018-10-25")
#     # x = df[df['expiry'] == date(2018,10,25)]
#     df = pd.DataFrame(data, columns=columns)
#     print(df.__len__())
#     # x = df[(df.expiry == date(2018, 10, 25))]
#     # print(x.__len__())
#     # x = x[x.timestamp == date(2018,10,22)]
#     # print(x.__len__())
#     # x = x[x.option_typ == 'CE']
#     # print(x.__len__())
#
#     expiry = [date(2018, 10, 25)]
#     timestamp = [date(2018, 10, 23)]
#     option_typ = ['CE']
#     y = df[df.expiry.isin(expiry) & df.timestamp.isin(timestamp) & df.option_typ.isin(option_typ)]
#     print(len(y))
#     # print(y['close'][0])
#     for row in y.itertuples():
#         print(row.strike)
#     # x = df.query("expiry == '2018-10-25'")
#     # print(x)
#     # print(df)
#     # print(df[df['expiry'] == date(2018,10,25)])
#     # print(df[df['timestamp'] == date(2018, 10, 22)])
#     # print(df[(df['option_typ'] == 'CE')])
#     print("Time: %s" % (time.time() - start_time))
#
#
# # download_url = 'https://www.nseindia.com/content/historical/DERIVATIVES/2018/OCT/fo23OCT2018bhav.csv.zip'
# browser, nseindia http refer
#
# if __name__ == '__main__':
#     start_time = time.time()
#     data = symbol_data("NIFTY", "2018-10-22", "2018-10-25")
#     # x = df[df['expiry'] == date(2018,10,25)]
#     df = pd.DataFrame(data, columns=columns)
#     print(df.__len__())
#     # x = df[(df.expiry == date(2018, 10, 25))]
#     # print(x.__len__())
#     # x = x[x.timestamp == date(2018,10,22)]
#     # print(x.__len__())
#     # x = x[x.option_typ == 'CE']
#     # print(x.__len__())
#
#     expiry = [date(2018, 10, 25)]
#     timestamp = [date(2018, 10, 23)]
#     option_typ = ['CE']
#     y = df[df.expiry.isin(expiry) & df.timestamp.isin(timestamp) & df.option_typ.isin(option_typ)]
#     print(len(y))
#     # print(y['close'][0])
#     for row in y.itertuples():
#         print(row.strike)
#     # x = df.query("expiry == '2018-10-25'")
#     # print(x)
#     # print(df)
#     # print(df[df['expiry'] == date(2018,10,25)])
#     # print(df[df['timestamp'] == date(2018, 10, 22)])
#     # print(df[(df['option_typ'] == 'CE')])
#     print("Time: %s" % (time.time() - start_time))

import time
from datetime import date, datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go

import options.database_connection as dbc
from constants import Keys

df = pd.DataFrame()

columns = ['id', 'instrument', 'symbol', 'expiry', 'strike', 'option_typ', 'open', 'high', 'low', 'close', 'settle_pr',
           'contracts', 'val', 'open_int', 'chg_in_oi', 'timestamp', 'iv', 'theta', 'gamma', 'delta', 'vega']
header_style = {'color': "white", "background": "black"}
# #FBF5CD
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dash_app.layout = html.Div([
    # dcc.Graph(id='graph-with-slider'),
    html.Table(children=[html.Tr(children=[
        html.Td(children=dcc.Input(
            id='scrip',
            placeholder='Enter the scrip...',
            type='text',
            value='NIFTY'
        ), ),
        html.Td(html.Button("Fetch", id="fetch"), ),
        html.Td(html.P(children='Not Ready', id='status'), )
    ]),
        html.Tr(children=[
            html.Td(dcc.Dropdown(
                id='expiry_list',
                options=[
                    # {'label': 'New York City', 'value': 'NYC'},
                ],
                placeholder='Expiry',
            ), ),
            html.Td(html.Button("Get", id="get_expiry"), ),
            html.Td(dcc.DatePickerSingle(
                id='date_picker',
                min_date_allowed=date(2018, 1, 2),
                max_date_allowed=date.today(),
                initial_visible_month=date(2017, 8, 5),
                date=date.today(),
                display_format="DD MMM YYYY"
            ), ),
            html.Td(
                html.Button("Display", id='display')
            ),
        ]),
    ]),
    html.P(id='info'),
    html.Table(id='market_watch')

])


@dash_app.callback(
    Output('status', 'children'),
    inputs=[Input('fetch', 'n_clicks')], state=[State('scrip', 'value')])
def fetch_data(n_clicks, scrip_name):
    global df
    if n_clicks is not None:
        scrip_name = scrip_name.capitalize()
        data = symbol_data(scrip_name)
        df = pd.DataFrame(data, columns=columns)
        # print(len(df))
        return "Ready"
    else:
        return "Not Ready"


@dash_app.callback(Output('expiry_list', 'options'), [Input('get_expiry', 'n_clicks')])
def get_expiry_list(n_clicks):
    global df
    expiry_list = []
    if n_clicks is not None:
        df_expiry = df.expiry.unique()
        # print(type(df_expiry))
        # print("Length of df_expiry %s" % len(df_expiry))
        for expiry_date in df_expiry.tolist():
            expiry_list.append({'label': expiry_date.strftime("%d %b %Y"), 'value': expiry_date})
    # print(expiry_list)
    return expiry_list


@dash_app.callback(Output('market_watch', 'children'), [Input('display', 'n_clicks')],
                   state=[State('expiry_list', 'value'), State('date_picker', 'date')])
def display_watch(n_clicks, expiry_date, obs_date):
    global df
    if n_clicks is not None:
        fmt = "%Y-%m-%d"
        expiry = [datetime.strptime(expiry_date, fmt).date()]
        timestamp = [datetime.strptime(obs_date, fmt).date()]
        option_call = [Keys.call]
        option_put = [Keys.put]
        call_data = df[df.expiry.isin(expiry) & df.timestamp.isin(timestamp) & df.option_typ.isin(option_call)]
        put_data = df[df.expiry.isin(expiry) & df.timestamp.isin(timestamp) & df.option_typ.isin(option_put)]
        strikes = []
        for row in call_data.itertuples():
            strikes.append(row.strike)

        table_rows = []
        v = ["Theta", "Gamma", "Delta", "Vega", "IV", "Close", "Contracts", "Change in OI", ]
        w = v.copy()
        w.reverse()
        table_header = v + ["Strike"] + w
        header = html.Tr([html.Td(head) for head in table_header], style=header_style)

        data = []
        z = [header]

        for strike in strikes:
            strike_row = []
            data_strike = []
            call = call_data[call_data.strike == strike]
            put = put_data[put_data.strike == strike]

            for ce in call.itertuples():
                x = [ce.theta, ce.gamma, ce.delta, ce.vega, ce.iv, ce.close, ce.contracts, ce.chg_in_oi, ]
                data_strike += x
                call_row = [html.Td(k, style={"background": "#FFCCFF"}) for k in x]
                strike_row.append(call_row)

            data_strike += [strike]
            strike_row[-1] += [html.Td(strike, style={"background": "#C2C2C2"})]

            for pe in put.itertuples():
                y = [pe.theta, pe.gamma, pe.delta, pe.vega, pe.iv, pe.close, pe.contracts, pe.chg_in_oi]
                y.reverse()
                data_strike += y
                put_row = [html.Td(k, style={"background": "#CCECFF"}) for k in y]
                strike_row[-1] += put_row

            data.append(data_strike)
            r = html.Tr(strike_row[0], style={"border": 2})
            # print(r)
            z.append(r)

        table_rows.append(header)
        for entry in data:
            row = html.Tr([html.Td(k) for k in entry], )
            table_rows.append(row)
            # print(row)
        # print(table_rows)
        # z = table_header + z
        return z


def symbol_data(symbol):
    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' " % (dbc.table_name, symbol,)
    option_data = dbc.execute_simple_query(option_query)
    return option_data


if __name__ == '__main__':
    dash_app.run_server()
    # fetch_data(1, "Nifty")
    # display_watch(1, "2018-10-25", "2018-10-23")
