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
    """
    It is used to analyse IV for a given list of strikes over the expiry.
    If a start date is not given then first day of the expiry month is taken.
    :param symbol: str
                Symbol for which analysis is to be done.
    :param strike_data: list[StrikeEntry]
                List of strikes for the analysis.
    :param expiry_month: int
                Expiry month for which back testing is to be done.
                For e.g. For month of 'October', 10 is input.
    :param expiry_year: int
                Year of the expiry month. This is included in case if database expands over multiple years.
                For e.g. 2018
    :param start_date: date
                Start date for the back testing. If none given, first of month is taken.
    :return: None
                Plots the underlying and strikes IV for the expiry.
    """
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
    for strike_entry in strike_data:
        if type(strike_entry) == StrikeEntry:
            option_expiry_df = option_df[
                (option_df.timestamp >= start_date) & (option_df.strike == strike_entry.strike) & (
                        option_df.option_typ == strike_entry.option_type)].sort_values('timestamp')
            ts_list = option_expiry_df.timestamp.values
            iv_list = option_expiry_df.iv.values
            iv_list[iv_list == 0] = None
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
        xaxis=dict(title='Timestamp', ),
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


def delta_iv_analysis(symbol: str, expiry_month: int, expiry_year: int, delta: float, delta_dev: float = 0.05,
                      start_date: date = None):
    """
    Used in the delta IV analysis of a symbol options for the expiry.
    :param symbol: str
                Symbol for which analysis is to be done.
    :param expiry_month: int
                Expiry month for which back testing is to be done.
                For e.g. For month of 'October', 10 is input.
    :param expiry_year: int
                Year of the expiry month. This is included in case if database expands over multiple years.
                For e.g. 2018
    :param delta: float
                Delta of the options for which IV is required to be plotted.
                Ranges from 0 to 1. For eg. 0.5
    :param delta_dev: float
                Deviation from the delta value given. Range is taken as (delta - delta_dev) and (delta + delta_dev)
                Defaults to 0.05
    :param start_date: date
                Start date for the analysis. If none given, first of month is taken.
    :return: None
                Plots the graph between IV and Timestamp at constant delta.
    """
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
    fut_df = fut_df[fut_df.timestamp >= start_date].sort_values('timestamp')
    option_df = option_df[option_df.timestamp >= start_date].sort_values('timestamp')

    delta_lower = delta - delta_dev
    delta_upper = delta + delta_dev

    timestamps_list = fut_df.timestamp.unique()
    fut_ts, fut_price = [], []
    call_ts, call_iv, call_text, = [], [], []
    put_ts, put_iv, put_text, = [], [], []
    for ts in timestamps_list:
        option_day_df = option_df[option_df.timestamp == ts]
        call_df = option_day_df[option_day_df.option_typ == Keys.call]
        put_df = option_day_df[option_day_df.option_typ == Keys.put]
        call_data = call_df[(call_df.delta >= delta_lower) & (call_df.delta <= delta_upper)].sort_values('delta',
                                                                                                         ascending=True)
        put_data = put_df[(put_df.delta >= -1 * delta_upper) & (put_df.delta <= -1 * delta_lower)].sort_values('delta',
                                                                                                               ascending=False)
        if len(call_data) > 0:
            data = call_data.iloc[0]
            iv = data.iv
            text = "%s%s %s" % (data.strike, data.option_typ, data.delta)
            call_ts.append(ts)
            call_iv.append(iv)
            call_text.append(text)

        if len(put_data) > 0:
            data = put_data.iloc[0]
            iv = data.iv
            text = "%s%s %s" % (data.strike, data.option_typ, data.delta)
            put_ts.append(ts)
            put_iv.append(iv)
            put_text.append(text)

        fut_close = fut_df[fut_df.timestamp == ts].iloc[0].close
        fut_ts.append(ts)
        fut_price.append(fut_close)

    call_trace = go.Scatter(x=call_ts, y=call_iv, text=call_text, name='CE')
    put_trace = go.Scatter(x=put_ts, y=put_iv, text=put_text, name='PE')
    fut_trace = go.Scatter(x=fut_ts, y=fut_price, name=symbol, yaxis='y2')

    traces = [call_trace, put_trace, fut_trace]

    layout = go.Layout(
        title='Delta IV Analysis',
        xaxis=dict(title='Timestamp', ),
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
    py.plot(fig, filename='delta_iv_analysis.html')


def iv_surface_analysis(symbol, expiry_month, expiry_year, start_strike, end_strike, gap: int = None,
                        start_date: date = None):
    """
    IV surface for the expiry for the given symbol.
    :param symbol: str
                Symbol for which analysis is to be done.
    :param expiry_month: int
                Expiry month for which back testing is to be done.
                For e.g. For month of 'October', 10 is input.
    :param expiry_year: int
                Year of the expiry month. This is included in case if database expands over multiple years.
                For e.g. 2018
    :param start_strike: int
                Starting strike for the Analysis
    :param end_strike: int
                Last strike for the Analysis
    :param gap: int
                Gap between the strikes to be taken.
    :param start_date: date
                Start date for the analysis. If none given, first of month is taken.
    :return: None
                Plots a 3D surface for the IV vs Strike vs Timestamp
    """
    symbol = symbol.upper()
    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    option_data = dbc.execute_simple_query(option_query)
    opt_df = pd.DataFrame(option_data, columns=dbc.columns)

    start_strike = int(start_strike) if start_strike is not None else None
    end_strike = int(end_strike) if end_strike is not None else None
    start_date = start_date if start_date else date(expiry_year, expiry_month, 1)

    opt_df = opt_df[
        (opt_df.strike >= start_strike) & (opt_df.strike <= end_strike) & (opt_df.timestamp >= start_date) & (
                    opt_df.iv <= 35.0)]
    # opt_df = opt_df[(opt_df.strike >= start_strike) & (opt_df.strike <= end_strike) & (opt_df.timestamp >= start_date)]

    if gap is not None:
        opt_df = opt_df[opt_df.strike % gap == 0]

    x = opt_df['strike'].values
    y = opt_df['timestamp'].values
    z = opt_df['iv'].values
    z[z == 0] = None
    # colorscale -> ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
    #  'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
    #  'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis']
    trace = go.Scatter3d(x=x, y=y, z=z,
                         marker=dict(
                             size=2,
                             color=z,
                             colorscale='Viridis',
                             opacity=1
                         ))
    data = [trace]
    layout = go.Layout(
        title='IV Surface',
        scene=dict(
            aspectmode="manual",
            # aspectratio=dict(x=10, y=4, z=5),
            xaxis=dict(
                title='Strike'
            ),
            yaxis=dict(
                title='Timestamp'
            ),
            zaxis=dict(
                title='IV',
                range=[0, 100],
            ), )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='iv_surface.html')


if __name__ == '__main__':
    strike_list = [StrikeEntry(10500, Keys.call),
                   StrikeEntry(10200, Keys.call),
                   StrikeEntry(10000, Keys.put),
                   StrikeEntry(11000, Keys.put)]
    # strike_vol_analysis("nifty", strike_list, 10, 2018, start_date=date(2018, 9, 27))
    # delta_iv_analysis("nifty", 10, 2018, 0.5)
    iv_surface_analysis("nifty", 9, 2018, 9500, 11500)
