import plotly.graph_objs as go
import plotly.offline as py


def get_candlestick_chart(data):
    trace_eod = go.Candlestick(x=data['date'],
                               open=data['open'],
                               high=data['high'],
                               low=data['low'],
                               close=data['close'])

    layout = dict(
        title='Historical EOD data',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=3,
                         label='3m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(count=3,
                         label='3y',
                         step='year',
                         stepmode='backward'),
                    dict(count=5,
                         label='5y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=False

            ),
            type='date'

        )
    )

    trace_sma = go.Scatter(
        x=data['date'],
        y=data['open'],
        name="SMA",
        line=dict(color='blue'),
        opacity=0.8)
    trace_sma01 = go.Scatter(
        x=data['date'],
        y=data['close'],
        name="EMA",
        line=dict(color='#9C00FF'),
        opacity=0.8)
    trace_sma02 = go.Scatter(
        x=data['date'],
        y=data['low'],
        name="SMA02",
        line=dict(color='#FF0062'),
        opacity=0.8)

    data01 = [trace_eod, trace_sma, trace_sma01, trace_sma02]

    fig = go.Figure(data=data01, layout=layout)
    py.offline.plot(fig, filename='simple-candlestick.html')
