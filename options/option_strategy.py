from datetime import date, timedelta

import numpy
import pandas as pd

from plotly import tools
import plotly.offline as py
import plotly.graph_objs as go

from constants import Keys
from model import StrikeEntry
from options import database_connection as dbc, payoff_charts


def options_strategy(symbol: str, strike_data: list, expiry_month: int, expiry_year: int, start_date: date,
                     spot_range: list, strategy_name: str = None):
    symbol = symbol.capitalize()
    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)
    fut_timeseries_data = [[], []]
    for fut_row in fut_df.itertuples():
        timestamp = fut_row.timestamp
        if timestamp >= start_date:
            fut_timeseries_data[0].append(timestamp)
            fut_timeseries_data[1].append(fut_row.close)
    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    option_data = dbc.execute_simple_query(option_query)
    option_df = pd.DataFrame(data=option_data, columns=dbc.columns)
    payoff_data = []
    for strikes in strike_data:
        strike = [strikes.strike]
        option_type = [strikes.option_type]
        strike_df = option_df[option_df.strike.isin(strike) & option_df.option_typ.isin(option_type)]
        init_day = strike_df[strike_df.timestamp == start_date]
        if len(init_day) > 0:
            init_price = init_day.close.values[0]
            for row in strike_df.itertuples():
                timestamp = row.timestamp
                close = row.close
                if timestamp >= start_date:
                    temp_pl = close - init_price
                    pl = temp_pl if strikes.signal == Keys.buy else (-1 * temp_pl)
                    payoff_data.append([timestamp, strikes.strike, strikes.option_type, pl])
        else:
            print("Couldn't find initial price for strike: %s%s and start date: %s" % (
                strikes.strike, strikes.option_type, start_date))

    if len(payoff_data) > 0:
        payoff_df = pd.DataFrame(payoff_data, columns=['timestamp', 'strike', 'option_typ', 'pl'])
        timestamp_cum_pl = [[], []]
        payoff_timestamp = payoff_df.timestamp.unique()
        for data_timestamp in payoff_timestamp:
            timestamp = [data_timestamp]
            timestamp_df = payoff_df[payoff_df.timestamp.isin(timestamp)]
            timestamp_pl = timestamp_df.pl.sum()
            timestamp_cum_pl[0].append(data_timestamp)
            timestamp_cum_pl[1].append(timestamp_pl)

        strike_cum_pl = []
        for strikes in strike_data:
            strike_time_series = [[], []]
            strike = [strikes.strike]
            option_type = [strikes.option_type]
            strike_payoff_df = payoff_df[payoff_df.strike.isin(strike) & payoff_df.option_typ.isin(option_type)]
            for item in strike_payoff_df.itertuples():
                strike_time_series[0].append(item.timestamp)
                strike_time_series[1].append(item.pl)
            strike_info = dict(
                strike=strikes.strike,
                option_type=strikes.option_type,
                signal=strikes.signal,
                timeseries=strike_time_series,
                df=strike_payoff_df,
            )
            strike_cum_pl.append(strike_info)
        spot, theoretical_payoff = _get_theoretical_payoffs(spot_range, strike_data)
        _plot_options_strategy_payoffs(symbol, fut_timeseries_data, timestamp_cum_pl, strike_cum_pl,
                                       [spot, theoretical_payoff], strategy_name)


def _get_theoretical_payoffs(spot: list, strike_data: list):
    spot = numpy.arange(min(spot), max(spot), 100, dtype=numpy.int64).tolist()
    payoff = []
    for strike in strike_data:
        if strike.premium:
            payoff_list = payoff_charts._get_payoff_values(spot, strike.strike, strike.option_type, strike.premium,
                                                           signal=strike.signal)
            # print(payoff_list)
            payoff.append(payoff_list)
        else:
            print("Parameter premium is required for %s for theoretical payoffs" % strike)

    while len(payoff) > 1:
        one = payoff[0]
        two = payoff[1]
        for i in range(len(one)):
            one[i] = one[i] + two[i]
        payoff.pop(1)

    if len(payoff) == 1:
        payoff = payoff[0]
    return spot, payoff


def _plot_options_strategy_payoffs(symbol, fut_timeseries_data, timestamp_cum_pl, strike_cum_pl, theoretical_pl,
                                   strategy_name: str = None):
    titles = []
    traces = []
    fut_period = fut_timeseries_data[0]
    fut_values = fut_timeseries_data[1]

    period = timestamp_cum_pl[0]
    values = timestamp_cum_pl[1]

    spot = theoretical_pl[0]
    payoff = theoretical_pl[1]

    # trace_fut = None
    if fut_period:
        name = 'Underlying %s' % symbol
        trace_fut = go.Scatter(x=fut_period, y=fut_values, name=symbol)
        titles.append(name)
        traces.append(trace_fut)

    if spot:
        name = 'Theoretical Payoffs'
        trace_payoff = go.Scatter(x=spot, y=payoff, name=name)
        titles.append(name)
        traces.append(trace_payoff)

    # trace_pl = None
    if period:
        name = 'Cumulative P&L'
        trace_pl = go.Scatter(x=period, y=values, name=name)
        titles.append(name)
        traces.append(trace_pl)

    for strike_pl in strike_cum_pl:
        strike = strike_pl['strike']
        opt_type = strike_pl['option_type']
        signal = strike_pl['signal']
        df = strike_pl['df']
        name = '%s%s' % (strike, opt_type)
        trace = go.Scatter(x=df['timestamp'], y=df['pl'], name=name)
        titles.append('%s %s' % (name, signal))
        traces.append(trace)

    # titles.append("Underlying vs Cum P&L")

    columns = 3
    len_traces = len(traces)
    # len_traces = len(traces) + 1
    rows = int(len_traces / columns) if len_traces % columns == 0 else (int(len_traces / columns) + 1)
    fig = tools.make_subplots(rows=rows, cols=columns, subplot_titles=titles)

    i = 0
    for row in range(rows):
        for col in range(columns):
            if i < len_traces:
                fig.append_trace(traces[i], row=row + 1, col=col + 1)
                i += 1

    # under_row = (int(len_traces / 3) + 1)
    # under_column = (len_traces % 3) + 1
    # print(under_row, under_column)
    # fig.append_trace(trace_fut, 2, 2)
    # fig.append_trace(trace_pl, 2, 2)
    # print(len_traces)
    # # print(fig)
    # fig['data'][-1].update(yaxis='y' + str(len_traces + 1))
    # fig['layout']['yaxis' + str(len_traces)].update(showgrid=True, title='Underlying')
    # fig['layout']['yaxis' + str(len_traces + 1)] = dict(overlaying='y' + str(len_traces), side='right', showgrid=False,
    #                                                     title='CUM P&L')
    # print(fig)

    title_name = '%s_payoffs' % (strategy_name if strategy_name else 'option_strategy')
    fig['layout'].update(title=title_name.capitalize())

    py.plot(fig, filename='%s.html' % title_name)


def oi_analytics(symbol: str, expiry_month: int, expiry_year: int, ):
    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)
    start_date = date(expiry_year, expiry_month, 1)
    x, y1, y2, y3 = [], [], [], []
    for fut_row in fut_df.itertuples():
        timestamp = fut_row.timestamp
        if timestamp >= start_date:
            # print(timestamp, fut_row.settle_pr, fut_row.open_int, fut_row.chg_in_oi)
            x.append(timestamp)
            y1.append(fut_row.open_int)
            y2.append(fut_row.settle_pr)
            y3.append(fut_row.chg_in_oi)
    trace1 = go.Scatter(x=x, y=y1, name='OI', )
    trace2 = go.Scatter(x=x, y=y2, name='settle_pr', yaxis='y2')
    trace3 = go.Scatter(x=x, y=y3, name='chg_in_oi', yaxis='y3', fill='tozeroy')

    data = [trace1, trace2, trace3]

    layout = go.Layout(
        title='OI Analytics',
        yaxis=dict(title='Open Interest', ),
        yaxis2=dict(
            title='Settle Price',
            anchor='free',
            overlaying='y',
            side='left',
            position=0.05
        ),
        yaxis3=dict(
            title='Change in OI',
            anchor='x',
            overlaying='y',
            side='right',
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='oi_analytics.html')


def put_call_ratio_expiry(symbol: str, expiry_month: int, expiry_year: int, ):
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
    option_expiry_df = option_df[option_df.timestamp >= start_date]
    timestamp_arr = option_expiry_df.timestamp.unique()
    call_option = [Keys.call]
    put_option = [Keys.put]
    x, y1, y2 = [], [], []
    for timestamp in timestamp_arr:
        day = [timestamp]
        call_df = option_expiry_df[option_expiry_df.option_typ.isin(call_option) & option_expiry_df.timestamp.isin(day)]
        put_df = option_expiry_df[option_expiry_df.option_typ.isin(put_option) & option_expiry_df.timestamp.isin(day)]
        call_volume = call_df.open_int.sum()
        put_volume = put_df.open_int.sum()
        pcr = put_volume / call_volume
        fut_price = fut_df[fut_df.timestamp.isin(day)].close.mean()
        # print(timestamp, fut_price, pcr)
        x.append(timestamp)
        y1.append(fut_price)
        y2.append(pcr)

    trace1 = go.Scatter(x=x, y=y1, name=symbol, )
    trace2 = go.Scatter(x=x, y=y2, name='PCR', yaxis='y2')
    # trace3 = go.Scatter(x=x, y=y3, name='chg_in_oi', yaxis='y3', fill='tozeroy')

    data = [trace1, trace2, ]

    layout = go.Layout(
        title='PCR Analytics',
        yaxis=dict(title='Underlying', ),
        yaxis2=dict(
            title='PCR',
            anchor='x',
            overlaying='y',
            side='right',
            position=0.05
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='pcr_expiry_analytics.html')


def put_call_ratio(symbol: str, ):
    symbol = symbol.capitalize()

    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' order by timestamp asc" % (
        dbc.table_name, symbol)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)

    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' order by timestamp asc" % (
        dbc.table_name, symbol)
    option_data = dbc.execute_simple_query(option_query)
    option_df = pd.DataFrame(data=option_data, columns=dbc.columns)

    expiry_dates = fut_df.sort_values('expiry').expiry.unique()
    call_option = [Keys.call]
    put_option = [Keys.put]
    x, y1, y2 = [], [], []
    init_expiry = None
    for expiry in expiry_dates:
        if init_expiry is None:
            init_expiry = date(expiry.year, expiry.month, 1)
        expiry_data = option_df[option_df.expiry == expiry]
        month_expiry_data = expiry_data[
            (expiry_data['timestamp'] >= init_expiry) & (expiry_data['timestamp'] <= expiry)]
        monthly_timestamps = month_expiry_data.timestamp.unique()
        for ts in monthly_timestamps:
            day = [ts]
            call_df = month_expiry_data[
                month_expiry_data.option_typ.isin(call_option) & month_expiry_data.timestamp.isin(day)]
            put_df = month_expiry_data[
                month_expiry_data.option_typ.isin(put_option) & month_expiry_data.timestamp.isin(day)]
            call_volume = call_df.open_int.sum()
            put_volume = put_df.open_int.sum()
            pcr = put_volume / call_volume
            fut_price = fut_df[fut_df.timestamp.isin(day)].close.mean()
            # print(ts, fut_price, pcr)
            x.append(ts)
            y1.append(fut_price)
            y2.append(pcr)

        # print(init_expiry, expiry)
        init_expiry = expiry + timedelta(days=1)

    trace1 = go.Scatter(x=x, y=y1, name=symbol, )
    trace2 = go.Scatter(x=x, y=y2, name='PCR', yaxis='y2')

    data = [trace1, trace2, ]

    layout = go.Layout(
        title='PCR Analytics',
        yaxis=dict(title='Underlying', ),
        yaxis2=dict(
            title='PCR',
            anchor='x',
            overlaying='y',
            side='right',
            position=0.05
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='pcr_analytics.html')


if __name__ == '__main__':
    strike_data = [
        StrikeEntry(Keys.buy, 10500, Keys.call, 368),
        StrikeEntry(Keys.buy, 10500, Keys.put, 222),
        # StrikeEntry(Keys.sell, 10200, Keys.call, 245),
        # StrikeEntry(10300, "CE", "BUY"),
        # StrikeEntry(10400, "CE", "SELL")
    ]
    # options_strategy("nifty", strike_data, 10, 2018, date(2018, 10, 1), spot_range=[9500, 11500])
    # oi_analytics("nifty", 10, 2018, )
    # put_call_ratio_expiry("nifty", 10, 2018, )
    put_call_ratio("nifty")
