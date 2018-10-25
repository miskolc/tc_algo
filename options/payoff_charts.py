from datetime import date

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt

import plotly.offline as py
import plotly.tools as tls

from options import option_greeks


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# payoff_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/'
#     'cb5392c35661370d95f300086accea51/raw/'
#     '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
#     'indicators.csv')
#
# available_indicators = df['Indicator Name'].unique()
#
# payoff_app.layout = html.Div([
#     html.Div([
#
#         html.Div([
#             dcc.Dropdown(
#                 id='crossfilter-xaxis-column',
#                 options=[{'label': i, 'value': i} for i in available_indicators],
#                 value='Fertility rate, total (births per woman)'
#             ),
#             dcc.RadioItems(
#                 id='crossfilter-xaxis-type',
#                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                 value='Linear',
#                 labelStyle={'display': 'inline-block'}
#             )
#         ],
#             style={'width': '49%', 'display': 'inline-block'}),
#
#         html.Div([
#             dcc.Dropdown(
#                 id='crossfilter-yaxis-column',
#                 options=[{'label': i, 'value': i} for i in available_indicators],
#                 value='Life expectancy at birth, total (years)'
#             ),
#             dcc.RadioItems(
#                 id='crossfilter-yaxis-type',
#                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                 value='Linear',
#                 labelStyle={'display': 'inline-block'}
#             )
#         ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
#     ], style={
#         'borderBottom': 'thin lightgrey solid',
#         'backgroundColor': 'rgb(250, 250, 250)',
#         'padding': '10px 5px'
#     }),
#
#     html.Div([
#         dcc.Graph(
#             id='crossfilter-indicator-scatter',
#             hoverData={'points': [{'customdata': 'Japan'}]}
#         )
#     ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
#     html.Div([
#         dcc.Graph(id='x-time-series'),
#         dcc.Graph(id='y-time-series'),
#     ], style={'display': 'inline-block', 'width': '49%'}),
#
#     html.Div(dcc.Slider(
#         id='crossfilter-year--slider',
#         min=df['Year'].min(),
#         max=df['Year'].max(),
#         value=df['Year'].max(),
#         marks={str(year): str(year) for year in df['Year'].unique()}
#     ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
# ])
#
#
# @payoff_app.callback(
#     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#     [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-year--slider', 'value')])
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]
#
#     return {
#         'data': [go.Scatter(
#             x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#             y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#             text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             mode='markers',
#             marker={
#                 'size': 15,
#                 'opacity': 0.5,
#                 'line': {'width': 0.5, 'color': 'white'}
#             }
#         )],
#         'layout': go.Layout(
#             xaxis={
#                 'title': xaxis_column_name,
#                 'type': 'linear' if xaxis_type == 'Linear' else 'log'
#             },
#             yaxis={
#                 'title': yaxis_column_name,
#                 'type': 'linear' if yaxis_type == 'Linear' else 'log'
#             },
#             margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
#             height=450,
#             hovermode='closest'
#         )
#     }
#
#
# def create_time_series(dff, axis_type, title):
#     return {
#         'data': [go.Scatter(
#             x=dff['Year'],
#             y=dff['Value'],
#             mode='lines+markers'
#         )],
#         'layout': {
#             'height': 225,
#             'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
#             'annotations': [{
#                 'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                 'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                 'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                 'text': title
#             }],
#             'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
#             'xaxis': {'showgrid': False}
#         }
#     }
#
#
# @payoff_app.callback(
#     dash.dependencies.Output('x-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
# def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#     country_name = hoverData['points'][0]['customdata']
#     dff = df[df['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)
#
#
# @payoff_app.callback(
#     dash.dependencies.Output('y-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)


def get_payoff_values(spot, strike: int, expiry_date: date, calculation_date: date, option_type: str,
                      option_price: float, volatility: float):
    delta_list, gamma_list, theta_list, vega_list, rho_list = [], [], [], [], []
    # spot = numpy.arange(9500, 11100, 100, dtype=numpy.int64).tolist()
    # strike = 10100
    # expiry_date = date(2018, 10, 25)
    # option_type = "CE"
    # option_price = 23.60
    # calculation_date = date(2018, 10, 23)
    # volatility = 23.60
    for underlying in spot:
        # print(underlying)
        delta, gamma, theta, vega, rho = option_greeks.get_option_greeks(underlying, strike, expiry_date, option_type,
                                                                         option_price, calculation_date, volatility)
        delta_list.append(delta)
        gamma_list.append(gamma)
        theta_list.append(theta)
        vega_list.append(vega)
        rho_list.append(rho)

    return delta_list, gamma_list, theta_list, vega_list, rho_list


if __name__ == '__main__':
    # app.run_server(port=8051)
    spot = numpy.arange(9500, 11100, 100, dtype=numpy.int64).tolist()
    strike = 10100
    expiry_date = date(2018, 10, 25)
    calculation_date = date(2018, 10, 15)
    option_type = "CE"
    option_price = 23.60
    volatility = 23.60
    delta_list, gamma_list, theta_list, vega_list, rho_list = get_payoff_values(spot, strike, expiry_date,
                                                                                calculation_date, option_type,
                                                                                option_price, volatility)

    # print(spot, delta_list, gamma_list, theta_list, vega_list, rho_list)

    fig = plt.figure()

    ax1 = fig.add_subplot(321)
    ax1.plot(spot, delta_list, 'r-')
    ax1.set_title('Delta')

    ax2 = fig.add_subplot(322)
    ax2.plot(spot, gamma_list, 'k-')
    ax2.set_title('Gamma')

    ax3 = fig.add_subplot(323)
    ax3.plot(spot, theta_list, 'b-')
    ax3.set_title('Theta')

    ax4 = fig.add_subplot(324)
    ax4.plot(spot, vega_list, 'g-')
    ax4.set_title('Vega')

    ax5 = fig.add_subplot(325)
    ax5.plot(spot, rho_list, )
    ax5.set_title('Rho')

    plt.tight_layout()
    fig = plt.gcf()

    plotly_fig = tls.mpl_to_plotly(fig)
    plotly_fig['layout']['title'] = 'Greeks Payoff Charts'
    plotly_fig['layout']['margin'].update({'t': 80})
    plotly_fig['layout']['height'] = 720
    plotly_fig['layout']['width'] = 1024

    py.plot(plotly_fig)
