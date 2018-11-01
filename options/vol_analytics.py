from datetime import date

from constants import Keys
from options import database_connection as dbc
import pandas as pd

import plotly.offline as py
import plotly.graph_objs as go


def strike_vol_analysis(symbol: str, strike: int, expiry_month: int, expiry_year: int, ):
    symbol = symbol.capitalize()
    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)

    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    option_data = dbc.execute_simple_query(option_query)
    option_df = pd.DataFrame(data=option_data, columns=dbc.columns)
    start_date = date(expiry_year, expiry_month, 1)
    option_expiry_df = option_df[(option_df.timestamp >= start_date) & (option_df.strike == strike)]
    timestamp_arr = option_expiry_df.timestamp.unique()
    call_option = [Keys.call]
    put_option = [Keys.put]
    x, y1, y2, y3 = [], [], [], []
    for timestamp in timestamp_arr:
        day = [timestamp]
        call_df = option_expiry_df[option_expiry_df.option_typ.isin(call_option) & option_expiry_df.timestamp.isin(day)]
        put_df = option_expiry_df[option_expiry_df.option_typ.isin(put_option) & option_expiry_df.timestamp.isin(day)]
        call_iv = call_df.iv.iloc[0]
        # call_iv = call_df.loc[call_df.index[0], 'iv']
        put_iv = put_df.iv.iloc[0]
        fut_price = fut_df[fut_df.timestamp.isin(day)].close.mean()
        x.append(timestamp)
        y1.append(call_iv)
        y2.append(put_iv)
        y3.append(fut_price)
        # print(timestamp, fut_price, call_iv, put_iv)

    trace1 = go.Scatter(x=x, y=y1, name='Call IV', )
    trace2 = go.Scatter(x=x, y=y2, name='Put IV', )
    trace3 = go.Scatter(x=x, y=y3, name='Underlying', yaxis='y2')
    # trace3 = go.Scatter(x=x, y=y3, name='chg_in_oi', yaxis='y3', fill='tozeroy')

    data = [trace1, trace2, trace3]

    layout = go.Layout(
        title='IV Analysis for %s %s, %s expiry' % (strike, expiry_month, expiry_year),
        yaxis=dict(title='IV', ),
        yaxis2=dict(
            title='Underlying',
            anchor='x',
            overlaying='y',
            side='right',
            position=0.05
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='strike_iv_analysis.html')


if __name__ == '__main__':
    strike_vol_analysis("nifty", 10500, 10, 2018)
