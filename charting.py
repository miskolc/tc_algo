import plotly.graph_objs as go
import plotly.offline as py


def get_candlestick_chart(data):
    trace = go.Candlestick(x=data['date'],
                           open=data['open'],
                           high=data['high'],
                           low=data['low'],
                           close=data['close'],
                           increasing=dict(line=dict(color='green')),
                           decreasing=dict(line=dict(color='red')))
    data01 = [trace]
    py.offline.plot(data01, filename='styled_candlestick.html')
