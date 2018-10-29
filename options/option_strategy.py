from datetime import date
import pandas as pd

from plotly import tools
import plotly.offline as py
import plotly.graph_objs as go

from model import StrikeEntry
from options import database_connection as dbc


def options_strategy(symbol: str, strike_data: list, expiry_month: int, expiry_year: int, start_date: date,
                     strategy_name: str = None):
    symbol = symbol.capitalize()
    option_query = "Select * from %s where symbol='%s' and instrument like 'OPT%%' and MONTH(expiry)=%d and YEAR(expiry)=%d" % (
        dbc.table_name, symbol, expiry_month, expiry_year)
    option_data = dbc.execute_simple_query(option_query)
    df = pd.DataFrame(data=option_data, columns=dbc.columns)
    payoff_data = []
    for strikes in strike_data:
        strike = [strikes.strike]
        option_type = [strikes.option_type]
        strike_df = df[df.strike.isin(strike) & df.option_typ.isin(option_type)]
        init_day = strike_df[strike_df.timestamp == start_date]
        if len(init_day) > 0:
            init_price = init_day.close.values[0]
            for row in strike_df.itertuples():
                timestamp = row.timestamp
                close = row.close
                if timestamp >= start_date:
                    temp_pl = close - init_price
                    pl = temp_pl if strikes.signal == "BUY" else (-1 * temp_pl)
                    payoff_data.append([timestamp, strikes.strike, strikes.option_type, pl])
        else:
            print("Couldn't find initial price for strike: %s%s and start date: %s" % (
                strikes.strike, strikes.option_type, start_date))

    if len(payoff_data) > 0:
        payoff_df = pd.DataFrame(payoff_data, columns=['timestamp', 'strike', 'option_typ', 'pl'])
        # print(payoff_df)
        timestamp_cum_pl = [[], []]
        payoff_timestamp = payoff_df.timestamp.unique()
        # print(payoff_timestamp)
        for data_timestamp in payoff_timestamp:
            timestamp = [data_timestamp]
            timestamp_df = payoff_df[payoff_df.timestamp.isin(timestamp)]
            timestamp_pl = timestamp_df.pl.sum()
            timestamp_cum_pl[0].append(data_timestamp)
            timestamp_cum_pl[1].append(timestamp_pl)
        # print(timestamp_cum_pl)

        strike_cum_pl = []
        for strikes in strike_data:
            strike_time_series = [[], []]
            strike = [strikes.strike]
            option_type = [strikes.option_type]
            strike_payoff_df = payoff_df[payoff_df.strike.isin(strike) & payoff_df.option_typ.isin(option_type)]
            for item in strike_payoff_df.itertuples():
                strike_time_series[0].append(item.timestamp)
                strike_time_series[1].append(item.pl)
            # print(strike, option_type, strike_payoff_df.pl.sum())
            strike_info = dict(
                strike=strikes.strike,
                option_type=strikes.option_type,
                signal=strikes.signal,
                timeseries=strike_time_series,
                df=strike_payoff_df,
            )
            strike_cum_pl.append(strike_info)
        # print(strike_pl)

        # print(timestamp_cum_pl)
        # print(strike_cum_pl)
        _plot_options_strategy_payoffs(timestamp_cum_pl, strike_cum_pl, strategy_name)


def _plot_options_strategy_payoffs(timestamp_cum_pl, strike_cum_pl, strategy_name: str = None):
    titles = []
    traces = []
    period = timestamp_cum_pl[0]
    values = timestamp_cum_pl[1]
    # print(period, values)
    if period:
        name = 'Cumulative P&L'
        trace = go.Scatter(x=period, y=values, name=name)
        titles.append(name)
        traces.append(trace)

    for strike_pl in strike_cum_pl:
        strike = strike_pl['strike']
        opt_type = strike_pl['option_type']
        signal = strike_pl['signal']
        df = strike_pl['df']
        name = '%s%s' % (strike, opt_type)
        trace = go.Scatter(x=df['timestamp'], y=df['pl'], name=name)
        titles.append('%s %s' % (name, signal))
        traces.append(trace)

    # print(titles)
    # print(traces)

    columns = 3
    len_traces = len(traces)
    rows = int(len_traces / columns) if len_traces % columns == 0 else (int(len_traces / columns) + 1)
    # print(rows)
    fig = tools.make_subplots(rows=rows, cols=columns, subplot_titles=titles)

    # i = 1
    # while i <= len_traces:
    #     row = 1
    #     while row <= row:
    #         col = 1
    #         while col <= columns:
    #             fig.append_trace(traces[i], row=row, col=col)

    i = 0
    for row in range(rows):
        for col in range(columns):
            if i < len_traces:
                fig.append_trace(traces[i], row=row + 1, col=col + 1)
                i += 1
    # trace1 = go.Scatter(x=[1, 2, 3], y=[4, 5, 6], name="")
    # trace2 = go.Scatter(x=[20, 30, 40], y=[50, 60, 70], name="")
    # trace3 = go.Scatter(x=[300, 400, 500], y=[600, 700, 800])
    # trace4 = go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000])
    #
    # fig = tools.make_subplots(rows=3, cols=3, subplot_titles=['Plot 1', 'Plot 2',
    #                                                           'Plot 3', 'Plot 4'])
    #
    # fig.append_trace(trace1, 1, 1)
    # fig.append_trace(trace2, 1, 2)
    # fig.append_trace(trace3, 1, 3)
    # fig.append_trace(trace4, 2, 1)
    # fig.append_trace(trace4, 2, 2)
    #
    title_name = '%s_payoffs' % (strategy_name if strategy_name else 'option_strategy')
    fig['layout'].update(title=title_name.capitalize())

    py.plot(fig, filename='%s.html' % title_name)


if __name__ == '__main__':
    strike_data = [
        StrikeEntry(10000, "CE", "BUY"),
        StrikeEntry(10200, "PE", "BUY"),
        StrikeEntry(10200, "CE", "SELL")
    ]
    options_strategy("nifty", strike_data, 10, 2018, date(2018, 10, 1))
    # _plot_options_strategy_payoffs([],[])
