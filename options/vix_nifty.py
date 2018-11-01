import mysql.connector
import pandas as pd

# from plotly import tools
import plotly.offline as py
import plotly.graph_objs as go

host = 'mysql7002.site4now.net'
user = 'l7oowjtp_abhish'
password = 'Bk7K=g+?ukBX'

db_name = 'l7oowjtp_tradingcampus2018'
table_name = 'eod_data'

NIFTY = 'Nifty 50'
VIX = 'India VIX'


# user l7oowjtp_abhish
# pass Bk7K=g+?ukBX
# database l7oowjtp_tradingcampus2018
# host mysql7002.site4now.net

def get_vix_nifty():
    db_conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = db_conn.cursor()
    query = "SELECT  date, symbol, close FROM `eod_data` WHERE (symbol='India VIX' OR symbol='NIFTY 50') order by date asc"
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['date', 'symbol', 'close'])
    nifty_df = df[df.symbol == NIFTY]
    vix_df = df[df.symbol == VIX]
    return nifty_df, vix_df


if __name__ == '__main__':
    nifty, vix = get_vix_nifty()
    trace_nifty = go.Scatter(x=nifty['date'], y=nifty['close'], name="Nifty 50")
    trace_vix = go.Scatter(x=vix['date'], y=vix['close'], name="India VIX", yaxis='y2')

    data = [trace_nifty, trace_vix]

    layout = go.Layout(
        title='Nifty50 vs India VIX',
        yaxis=dict(title='Nifty50', ),
        yaxis2=dict(
            title='India VIX',
            anchor='x',
            overlaying='y',
            side='right',
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='nifty_vs_vix.html')
