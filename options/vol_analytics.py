from datetime import date
from typing import List

from constants import Keys
from model import StrikeEntry
from options import database_connection as dbc
import pandas as pd

import plotly.offline as py
import plotly.graph_objs as go


def strike_vol_analysis(symbol: str, strike_data: List[StrikeEntry], expiry_month: int, expiry_year: int,
                        start_date: date = None):
    symbol = symbol.upper()
    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)

    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    option_data = dbc.execute_simple_query(option_query)
    option_df = pd.DataFrame(data=option_data, columns=dbc.columns)

    start_date = start_date if start_date else date(expiry_year, expiry_month, 1)
    traces = []
    # option_data = []
    for strike_entry in strike_data:
        if type(strike_entry) == StrikeEntry:
            option_expiry_df = option_df[
                (option_df.timestamp >= start_date) & (option_df.strike == strike_entry.strike) & (
                        option_df.option_typ == strike_entry.option_type)].sort_values('timestamp')
            ts_list = option_expiry_df.timestamp.values
            iv_list = option_expiry_df.iv.values
            name = "%s%s" % (strike_entry.strike, strike_entry.option_type)
            trace = go.Scatter(x=ts_list, y=iv_list, name=name)
            traces.append(trace)
        else:
            print("Expected a %s got %s instead" % (StrikeEntry, type(strike_entry)))
            return

    fut_df = fut_df[fut_df.timestamp >= start_date].sort_values('timestamp')
    timestamp_list = fut_df.timestamp.unique()
    underlying_values = fut_df[fut_df.timestamp >= start_date].sort_values('timestamp').close.values
    fut_trace = go.Scatter(x=timestamp_list, y=underlying_values, name=symbol, yaxis='y2')
    traces.append(fut_trace)

    layout = go.Layout(
        title='IV Analysis',
        yaxis=dict(title='IV', ),
        yaxis2=dict(
            title='Underlying',
            anchor='x',
            overlaying='y',
            side='right',
            position=0.05
        ),
    )
    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename='strike_iv_analysis.html')


if __name__ == '__main__':
    strike_list = [StrikeEntry(10500, Keys.call),
                   StrikeEntry(10200, Keys.call),
                   StrikeEntry(10000, Keys.put),
                   StrikeEntry(11000, Keys.put)]
    strike_vol_analysis("nifty", strike_list, 10, 2018, start_date=date(2018, 9, 27))
