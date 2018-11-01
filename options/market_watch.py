import time
from datetime import date, datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

import options.database_connection as dbc
from constants import Keys

fut_df = pd.DataFrame()
opt_df = pd.DataFrame()

strikes = []
call_oi = []
put_oi = []
call_iv = []
put_iv = []

header_style = {'color': "white", "background": "black"}
border = "2px solid black"
itm_color = '#FBF5CD'
call_color = "#FFCCFF"
put_color = "#CCECFF"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

market_watch_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

market_watch_app.layout = html.Div([
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
    html.Br(),
    html.Div(id='oi_container', children=[
        html.Button("OI", id='oi'),
        html.P(id='oi_status'),
        html.Button("IV", id='iv'),
        html.P(id='iv_status')
    ]),
    html.Br(),
    html.Table(id='market_watch')
])


@market_watch_app.callback(
    Output('status', 'children'),
    inputs=[Input('fetch', 'n_clicks')], state=[State('scrip', 'value')])
def fetch_data(n_clicks, scrip_name):
    """
    It fetches the data initially when button is clicked
    :param n_clicks: int
            Button clicks for the button id fetch
    :param scrip_name: str
            Name of the scrip for which data is required.
    :return: status of the data
    """
    global fut_df, opt_df
    if n_clicks is not None:
        scrip_name = scrip_name.upper()
        future_data, option_data = _symbol_data(scrip_name)
        fut_df = pd.DataFrame(future_data, columns=dbc.columns)
        opt_df = pd.DataFrame(option_data, columns=dbc.columns)
        return "Ready"
    else:
        return "Not Ready"


@market_watch_app.callback(Output('expiry_list', 'options'), [Input('get_expiry', 'n_clicks')])
def get_expiry_list(n_clicks):
    """
    Gets the expiry list for the symbol
    :param n_clicks: int
            Button clicks for the button id get_expiry
    :return: list of date of expiry
    """
    global fut_df
    expiry_list = []
    if n_clicks is not None:
        df_expiry = fut_df.sort_values('expiry').expiry.unique()
        for expiry_date in df_expiry.tolist():
            expiry_list.append({'label': expiry_date.strftime("%d %b %Y"), 'value': expiry_date})
    return expiry_list


@market_watch_app.callback(Output('market_watch', 'children'), [Input('display', 'n_clicks')],
                           state=[State('expiry_list', 'value'), State('date_picker', 'date')])
def display_watch(n_clicks, expiry_date, obs_date):
    """
    This is used to display match watch contents after selection of expiry and observation date.
    :param n_clicks: int
            Button clicks for the id 'display'
    :param expiry_date: str
            Expiry date
    :param obs_date: str
            Observation date
    :return: table rows to be displayed to table id market_watch
    """
    global opt_df, fut_df, strikes, call_oi, put_oi, call_iv, put_iv
    if n_clicks is not None:
        fmt = "%Y-%m-%d"
        expiry = [datetime.strptime(expiry_date, fmt).date()]
        timestamp = [datetime.strptime(obs_date, fmt).date()]
        option_call = [Keys.call]
        option_put = [Keys.put]
        fut_data = fut_df[fut_df.expiry.isin(expiry) & fut_df.timestamp.isin(timestamp)]
        # print("Fut data: %s" % fut_data)
        underlying = None
        try:
            # underlying = fut_data.close[0]
            # print(underlying)
            for udrly in fut_data.itertuples():
                underlying = udrly.close
        except (KeyError, IndexError):
            # print("Error")
            pass

        call_data = opt_df[
            opt_df.expiry.isin(expiry) & opt_df.timestamp.isin(timestamp) & opt_df.option_typ.isin(option_call)]
        put_data = opt_df[
            opt_df.expiry.isin(expiry) & opt_df.timestamp.isin(timestamp) & opt_df.option_typ.isin(option_put)]
        strikes = []
        call_oi = []
        put_oi = []
        call_iv = []
        put_iv = []
        for row in call_data.itertuples():
            strikes.append(row.strike)

        v = ["Theta", "Gamma", "Delta", "Vega", "IV", "Close", "Contracts", "Change in OI", ]
        w = v.copy()
        w.reverse()
        table_header = v + ["Strike"] + w
        header = html.Tr([html.Td(head) for head in table_header], style=header_style)

        table_rows = [header]

        # print(underlying)
        if underlying is not None:
            for strike in strikes:
                strike_row = []
                itm = True if strike < underlying else False

                call = call_data[call_data.strike == strike]
                put = put_data[put_data.strike == strike]

                for ce in call.itertuples():
                    x = [ce.theta, ce.gamma, ce.delta, ce.vega, ce.iv, ce.close, ce.contracts, ce.chg_in_oi, ]
                    call_oi.append(ce.open_int)
                    call_iv.append(ce.iv)
                    call_row = [html.Td(k, style={"background": itm_color if itm else call_color, }) for k in x]
                    strike_row.append(call_row)

                strike_row[-1] += [html.Td(strike, style={"background": "#C2C2C2", "border": border})]

                for pe in put.itertuples():
                    y = [pe.theta, pe.gamma, pe.delta, pe.vega, pe.iv, pe.close, pe.contracts, pe.chg_in_oi]
                    put_oi.append(pe.open_int)
                    put_iv.append(pe.iv)
                    y.reverse()
                    put_row = [html.Td(k, style={"background": put_color if itm else itm_color}) for k in y]
                    strike_row[-1] += put_row

                row = html.Tr(strike_row[0], style={"border": border})
                table_rows.append(row)

        return table_rows


@market_watch_app.callback(
    Output('oi_status', 'children'),
    inputs=[Input('oi', 'n_clicks')], )
def display_oi(n_clicks):
    """
    This used to display the oi bar chart for call and put using plotly.
    :param n_clicks: int
            Button clicks for id oi_status
    :return: None
    """
    global strikes, call_oi, put_oi
    if n_clicks is not None:
        trace1 = go.Bar(
            x=strikes,
            y=call_oi,
            name="Call OI",
            textposition='outside',
        )

        trace2 = go.Bar(
            x=strikes,
            y=put_oi,
            name="Put OI",
            textposition='outside',
        )

        data = [trace1, trace2]
        layout = go.Layout(
            title='OI Analysis',
            xaxis=dict(tickangle=-45),
            barmode='group',
        )
        fig = go.Figure(data=data, layout=layout)

        py.plot(fig, filename='oi_chart.html')
        return "Displaying OI..."


@market_watch_app.callback(
    Output('iv_status', 'children'),
    inputs=[Input('iv', 'n_clicks')], )
def display_iv(n_clicks):
    """
    This used to display the oi bar chart for call and put using plotly.
    :param n_clicks: int
            Button clicks for id oi_status
    :return: None
    """
    global strikes, call_iv, put_iv
    if n_clicks is not None:
        trace1 = go.Scatter(x=strikes, y=call_iv, name="Call IV")
        trace2 = go.Scatter(x=strikes, y=put_iv, name="Put IV")

        data = [trace1, trace2]
        layout = go.Layout(
            title='IV Graph',
            xaxis=dict(tickangle=-45),
        )
        fig = go.Figure(data=data, layout=layout)

        py.plot(fig, filename='iv_chart.html')
        return "Displaying IV..."


def _symbol_data(symbol):
    """
    It get the data for the given symbol
    :param symbol: str
            Symbol for which data is required. eg. NIFTY
    :return: tuple(list, list)
            Returns futures data and options data
    """
    print("Fetching data...")
    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' " % (dbc.table_name, symbol,)
    option_data = dbc.execute_simple_query(option_query)
    future_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' " % (dbc.table_name, symbol,)
    future_data = dbc.execute_simple_query(future_query)
    # print(len(option_data), len(future_data))
    return future_data, option_data


def get_market_watch_app():
    """
    It returns a dash app which can be run as market watch app.
    :return: dash app
            Dash app for market watch display
    """
    # dash_app.run_server()
    # fetch_data(1, "Nifty")
    # get_expiry_list(1)
    # display_watch(1, "2018-10-25", "2018-10-23")
    # display_oi(1)
    return market_watch_app
