import json
from datetime import datetime

import mysql.connector
import pandas as pd

import plotly.offline as py
import plotly.graph_objs as go
import requests

from options import option_strategy

host = 'mysql7002.site4now.net'
user = 'l7oowjtp_abhish'
password = 'Bk7K=g+?ukBX'

db_name = 'l7oowjtp_tradingcampus2018'
table_name = 'eod_data'
NIFTY = 'Nifty 50'
VIX = 'India VIX'
data_url = "http://l7oowjtp-site.gtempurl.com/python_data/nifty_vix.php"


# def get_vix_nifty_data():
#     """
#     This function is used to fetch data from the server for India VIX and Nifty
#     :return: Tuple(DataFrame, DataFrame)
#             Nifty DataFrame, VIX DataFrame
#     """
#     db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
#     cursor = db_conn.cursor()
#     query = "SELECT  date, symbol, close FROM `eod_data` WHERE (symbol='India VIX' OR symbol='NIFTY 50') order by date asc"
#     cursor.execute(query)
#     result = cursor.fetchall()
#     df = pd.DataFrame(result, columns=['date', 'symbol', 'close'])
#     nifty_df = df[df.symbol == NIFTY]
#     vix_df = df[df.symbol == VIX]
#     db_conn.close()
#     return nifty_df, vix_df

def get_vix_nifty_data():
    """
    This function is used to fetch data from the server for India VIX and Nifty
    :return: Tuple(DataFrame, DataFrame)
            Nifty DataFrame, VIX DataFrame
    """
    result1 = requests.get(data_url)
    content = json.loads(result1.content)
    data = []
    for element in content:
        date_value = datetime.strptime(element[0], "%Y-%m-%d").date()
        close = float(element[2])
        data.append((date_value, element[1], close))
    df = pd.DataFrame(data, columns=['date', 'symbol', 'close'])
    nifty_df = df[df.symbol == NIFTY]
    vix_df = df[df.symbol == VIX]
    return nifty_df, vix_df


def vix_nifty_plot():
    """
    It is used to plot the data for Nifty and India VIX
    :return: None
            Plots a chart for nifty and vix
    """
    nifty, vix = get_vix_nifty_data()
    trace_vix = go.Scatter(x=vix['date'], y=vix['close'], name="India VIX")
    trace_nifty = go.Scatter(x=nifty['date'], y=nifty['close'], name="Nifty 50", yaxis='y2')

    dates = nifty['date'].values
    date_begin = dates[0]
    date_end = dates[-1]
    avg_vix = vix.close.mean()
    data = [trace_vix, trace_nifty]

    layout = go.Layout(
        title='India VIX vs Nifty',
        yaxis=dict(title='India VIX', showgrid=False),
        yaxis2=dict(
            title='Nifty50',
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False,
        ),
        shapes=[{
            'type': 'line',
            'x0': date_begin,
            'y0': avg_vix,
            'x1': date_end,
            'y1': avg_vix,
            'line': {
                'color': 'rgb(50, 171, 96)',
                'width': 2,
                'dash': 'dashdot',
            },
        }, ]
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='vix_vs_nifty.html')


def vix_nifty_pcr_plot():
    """
    It is used to plot the data for Nifty and India VIX and PCR
    :return: None
            Plots a chart for nifty and vix and PCR
    """
    nifty, vix = get_vix_nifty_data()
    trace_vix = go.Scatter(x=vix['date'], y=vix['close'], name="India VIX")
    trace_nifty = go.Scatter(x=nifty['date'], y=nifty['close'], name="Nifty 50", yaxis='y2')

    dates = nifty['date'].values
    date_begin = dates[0]
    date_end = dates[-1]
    avg_vix = vix.close.mean()

    pcr_timestamps, pcr_data = option_strategy.put_call_ratio('nifty', data_only=True)
    # print(pcr_timestamps[0], pcr_timestamps[-1], len(pcr_data))
    trace_pcr = go.Scatter(x=pcr_timestamps, y=pcr_data, name='PCR', yaxis='y3')
    data = [trace_vix, trace_nifty, trace_pcr]

    layout = go.Layout(
        title='India VIX vs Nifty',
        yaxis=dict(title='India VIX', showgrid=False),
        yaxis2=dict(
            title='Nifty50',
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False,
        ),
        yaxis3=dict(
            title='PCR',
            anchor='x',
            overlaying='y',
            side='right',
            position=0.25,
        ),
        shapes=[{
            'type': 'line',
            'x0': date_begin,
            'y0': avg_vix,
            'x1': date_end,
            'y1': avg_vix,
            'line': {
                'color': 'rgb(255, 35, 35)',
                'width': 2,
                'dash': 'dashdot',
            },
        }, ]
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='vix_vs_nifty_vs_pcr.html')
