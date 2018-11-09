from datetime import date, timedelta
from typing import List

import numpy
import pandas as pd

from plotly import tools
import plotly.offline as py
import plotly.graph_objs as go

from constants import Keys
from model import StrikeEntry
from options import database_connection as dbc, payoff_charts


def options_strategy(symbol: str, strike_data: List[StrikeEntry], expiry_month: int, expiry_year: int, start_date: date,
                     spot_range: list, strategy_name: str = None):
    """
    Used for the analysis and back testing of the strikes for the period of the expiry.
    It plots theoretical payoffs along with the individual payoff for each strike over the time of expiry.
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
    :param spot_range: list
                Values required for the calculating theoretical payoffs. for eg. [9500, 11000]
    :param strategy_name: str
                Name of the strategy
    :return: None
                Plots the different payoffs for the strategy inputs.
    """
    symbol = symbol.upper()
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
        if type(strikes) == StrikeEntry:
            strike = [strikes.strike]
            option_type = [strikes.option_type]
            strike_df = option_df[option_df.strike.isin(strike) & option_df.option_typ.isin(option_type)]
            init_day_entry = strike_df[strike_df.timestamp == start_date]
            if (len(init_day_entry) > 0) & (strikes.signal in [Keys.buy, Keys.sell]):
                init_price = init_day_entry.close.values[0]
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
        else:
            print("Input can be only be of type %s given %s" % (StrikeEntry, type(strikes)))
            return

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
    """
    Helper function for getting theoretical payoffs
    :param spot: list
            Range of Spot values
    :param strike_data: list[StrikeEntry]
            Strike entry for the theoretical payoffs
    :return: tuple(list, list)
            Returns spot values and corresponding payoffs
    """
    spot = numpy.arange(min(spot), max(spot), 100, dtype=numpy.int64).tolist()
    payoff = []
    for strike in strike_data:
        premium = strike.premium if strike.premium else 100
        if premium:
            payoff_list = payoff_charts._get_payoff_values(spot, strike.strike, strike.option_type, premium,
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
    """
    Helper function for plotting payoff diagrams in option strategy
    :param symbol: str
                Symbol under analysis
    :param fut_timeseries_data: list
                Data for plotting underlying future price
    :param timestamp_cum_pl: list
                Data for plotting cumulative profit and loss
    :param strike_cum_pl: list
                Data for plotting individual strike profit and loss
    :param theoretical_pl: list
                Data for plotting theoretical payoffs
    :param strategy_name: str
                Name of the strategy
    :return: None
                Plots the input data
    """
    titles = []
    traces = []
    fut_period = fut_timeseries_data[0]
    fut_values = fut_timeseries_data[1]

    period = timestamp_cum_pl[0]
    values = timestamp_cum_pl[1]

    spot = theoretical_pl[0]
    payoff = theoretical_pl[1]

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

    columns = 3
    len_traces = len(traces)
    rows = int(len_traces / columns) if len_traces % columns == 0 else (int(len_traces / columns) + 1)
    fig = tools.make_subplots(rows=rows, cols=columns, subplot_titles=titles)

    i = 0
    for row in range(rows):
        for col in range(columns):
            if i < len_traces:
                fig.append_trace(traces[i], row=row + 1, col=col + 1)
                i += 1

    title_name = '%s_payoffs' % (strategy_name if strategy_name else 'option_strategy')
    fig['layout'].update(title=title_name.upper())

    py.plot(fig, filename='%s.html' % title_name)


def oi_analytics(symbol: str, expiry_month: int, expiry_year: int, start_date: date = None):
    """
    Used for the OI Analytics of the symbol over the period of expiry
    :param symbol: str
                Symbol for which analysis is to be done.
    :param expiry_month: int
                Expiry month for which back testing is to be done.
                For e.g. For month of 'October', 10 is input.
    :param expiry_year: int
                Year of the expiry month. This is included in case if database expands over multiple years.
                For e.g. 2018
    :param start_date: date
                Start date for the back testing. If none given, first of month is taken.
    :return: None
                Plots the graph for oi analysis. Underlying, OI and Change in OI.
    """
    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)
    start_date = start_date if start_date else date(expiry_year, expiry_month, 1)
    x, y1, y2, y3 = [], [], [], []
    for fut_row in fut_df.itertuples():
        timestamp = fut_row.timestamp
        if timestamp >= start_date:
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


def put_call_ratio_expiry(symbol: str, expiry_month: int, expiry_year: int, start_date: date = None):
    """
    Used for the PCR Analytics of the symbol over the period of expiry
    :param symbol: str
                Symbol for which analysis is to be done.
    :param expiry_month: int
                Expiry month for which back testing is to be done.
                For e.g. For month of 'October', 10 is input.
    :param expiry_year: int
                Year of the expiry month. This is included in case if database expands over multiple years.
                For e.g. 2018
    :param start_date: date
                Start date for the back testing. If none given, first of month is taken.
    :return: None
                Plots the graph for PCR analysis. Underlying, and PCR are plotted.
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
    option_expiry_df = option_df[option_df.timestamp >= start_date].sort_values('timestamp')
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
        x.append(timestamp)
        y1.append(fut_price)
        y2.append(pcr)

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
    py.plot(fig, filename='pcr_expiry_analytics.html')


def put_call_ratio(symbol: str, ):
    """
    Used for plotting the PCR ratio fot the symbol for all the expiry available in the database
    :param symbol: str
                Symbol for which PCR is required.
    :return: None
                Plots the PCR graph for the symbol along with underlying
    """
    symbol = symbol.upper()

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
            x.append(ts)
            y1.append(fut_price)
            y2.append(pcr)

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


def max_pain(symbol: str, expiry_month: int, expiry_year: int, start_strike: int, end_strike: int, gap: int = None,
             start_date: date = None, last_date: date = None, timestamp: date = None):
    """
    It is used to analyse the max pain for either a day or few days.
    If start date, last date and timestamp are given then timestamp is given preference.
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
                Start date for the back testing. If none given, first of month is taken.
    :param last_date: date
                Last date of the observation. if none is given then expiry day is taken.
    :param timestamp: date
                Day for which Max Pain is to be observed.
    :return: None
                Table is displayed showing Max pain strikes along with underlying
                Plots a bar chart if timestamp is given.
    """
    symbol = symbol.upper()

    fut_query = "Select * from %s where symbol='%s' and instrument like 'FUT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d order by timestamp asc" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    fut_data = dbc.execute_simple_query(fut_query)
    fut_df = pd.DataFrame(data=fut_data, columns=dbc.columns)

    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d order by timestamp asc" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    option_data = dbc.execute_simple_query(option_query)
    option_df = pd.DataFrame(data=option_data, columns=dbc.columns)

    start_date = start_date if start_date else date(expiry_year, expiry_month, 1)
    fut_df = fut_df[fut_df.timestamp >= start_date]
    option_df = option_df[
        (option_df.timestamp >= start_date) & (option_df.strike >= start_strike) & (option_df.strike <= end_strike)]

    if last_date is not None:
        fut_df = fut_df[fut_df.timestamp <= last_date]
        option_df = option_df[option_df.timestamp <= last_date]

    if gap is not None:
        option_df = option_df[option_df.strike % gap == 0]

    if timestamp is not None:
        fut_df = fut_df[fut_df.timestamp == timestamp]
        option_df = option_df[option_df.timestamp == timestamp]

    days_arr = fut_df.timestamp.unique()
    timestamp_values = []
    table_ts, table_underlying, table_max_pain_strikes = [], [], []
    for ts in days_arr:
        call_df = option_df[(option_df.timestamp == ts) & (option_df.option_typ == Keys.call)]
        put_df = option_df[(option_df.timestamp == ts) & (option_df.option_typ == Keys.put)]
        call_strikes = call_df.strike.unique()
        put_strikes = put_df.strike.unique()
        strikes = list(set(call_strikes).intersection(set(put_strikes)))
        strikes.sort()

        if strikes is not None:
            diff_call = []
            for strike in strikes:
                diff_call.append(strike - strikes[0])
            diff_put = diff_call.copy()
            diff_put.reverse()

            timestamp_values = []
            for i in range(len(strikes)):
                strike = strikes[i]
                call_oi = call_df[call_df.strike == strike].open_int.values[0]
                call_money = diff_call[i] * call_oi
                put_oi = put_df[put_df.strike == strike].open_int.values[0]
                put_money = diff_put[i] * put_oi
                strike_money = call_money + put_money
                timestamp_values.append([strike, strike_money])
            values = timestamp_values.copy()
            values.sort(key=lambda x: x[1])
            values = values[:5]
            max_pain_strikes = [item[0] for item in values]
            underlying = fut_df[fut_df.timestamp == ts].close.values[0]
            # print(ts, underlying, max_pain_strikes)
            table_ts.append(ts)
            table_underlying.append(underlying)
            table_max_pain_strikes.append(max_pain_strikes)

    x, y = [], []
    for value in timestamp_values:
        x.append(value[0])
        y.append(value[1])
    if timestamp is not None:
        if len(x) > 0:
            trace = go.Bar(x=x, y=y)
            data = [trace]
            layout = go.Layout(
                title="%s Max Pain for %s" % (symbol, timestamp),

            )
            fig = go.Figure(data, layout=layout)
            py.plot(fig, filename='max_pain.html')
        else:
            print("No data for plotting for %s" % timestamp)

    table_header = ['Timestamp', 'Underlying', 'Strikes with max pain']
    table_trace = go.Table(
        header=dict(values=table_header,
                    line=dict(color='#7D7F80'),
                    fill=dict(color='#a1c3d1'),
                    ),
        cells=dict(values=[table_ts, table_underlying, table_max_pain_strikes],
                   line=dict(color='#7D7F80'),
                   fill=dict(color='#EDFAFF'),
                   )
    )

    data_table = [table_trace]
    layout_table = go.Layout(
        title="%s Max Pain for %s,%s" % (symbol, expiry_month, expiry_year),
    )
    fig = dict(data=data_table, layout=layout_table)
    py.plot(fig, filename="max_pain_report.html")


if __name__ == '__main__':
    strike_data = [
        StrikeEntry(26100, Keys.call, Keys.buy, ),
        StrikeEntry(26100, Keys.put, Keys.buy, ),
        StrikeEntry(26200, Keys.call, Keys.sell, ),
        StrikeEntry(26200, Keys.put, Keys.sell, ),

    ]
    # options_strategy("banknifty", strike_data, 10, 2018, date(2018, 10, 1), spot_range=[25000, 27000])
    # oi_analytics("nifty", 10, 2018, )
    # put_call_ratio_expiry("nifty", 10, 2018, )
    # put_call_ratio("nifty")
    # max_pain("nifty", 10, 2018, )
    # max_pain(symbol="nifty", expiry_month=10, expiry_year=2018, start_strike=9500, end_strike=11500, gap=100, )
    # max_pain(symbol="nifty", expiry_month=10, expiry_year=2018, start_strike=9500, end_strike=11500, gap=100, timestamp=date(2018, 10, 22))
    max_pain(symbol="nifty", expiry_month=10, expiry_year=2018, start_strike=9500, end_strike=11500, gap=100,
             start_date=date(2018, 9, 15), last_date=date(2018, 10, 15))
