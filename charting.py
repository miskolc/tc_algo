from flask import Flask, render_template, url_for

import constants as ct

"""
List of Chart:
1. Chart with indicators
2. BackTest with Annotation (Buy and Sell)
3. BackTest Report - Cum P&L all
                   - Cum P&L Long
                   - Cum P&L Short
"""
result = {}
app = Flask(__name__, )


def create_app(input_result):
    """
    It creates a Flask App.
    :param input_result: result to be plotted
    :return: Flask App
    """
    app.config.from_pyfile('config.py', silent=True)
    app.debug = True
    app.templates_auto_reload = False
    global result
    result = input_result
    # app.add_url_rule(rule='/', endpoint="index", view_func=index("Hello"))
    return app


@app.route("/")
def chart_template():
    """
    For plotting normal candle chart or along with indicators
    :return: None
    """
    if (result.__contains__(ct.key_data_prop)) & (result.__contains__(ct.key_data)) & (
            result.__contains__(ct.key_params)):
        data_properties = result[ct.key_data_prop]
        main_chart = []
        for key, values in data_properties.items():
            main_chart.append([key, values])
        params = result[ct.key_params]
        data_list = result[ct.key_data]
        return render_template("chart.html", chartData=data_list, chart_params=params, main_chart_properties=main_chart)


@app.route("/backtest/")
def back_test_template():
    """
    For plotting back test chart with annotations.
    :return: None
    """
    if (result.__contains__(ct.key_data_prop)) & (result.__contains__(ct.key_data)) & (
            result.__contains__(ct.key_params)) & (result.__contains__(ct.key_annotations)):
        data_properties = result[ct.key_data_prop]
        main_chart = []
        for key, values in data_properties.items():
            main_chart.append([key, values])
        params = result[ct.key_params]
        data_list = result[ct.key_data]
        annotations = result[ct.key_annotations]
        return render_template("backtest.html", chartData=data_list, chart_params=params,
                               main_chart_properties=main_chart, chart_annotations=annotations)


@app.route("/bt_report_all/")
def cum_pl_all():
    """
    Chart for back test reports of Cumulative profit and loss for all strategies
    :return: None
    """
    if (result.__contains__(ct.key_all)) & (result.__contains__(ct.key_data_prop)):
        cum_all = result[ct.key_all][ct.key_date_cum_pl]
        data_properties = result[ct.key_data_prop]
        bt_chart = []
        for key, values in data_properties.items():
            bt_chart.append([key, values])
        return render_template("cum_pl_all.html", chartData=cum_all, bt_chart_properties=bt_chart)


@app.route("/bt_report_long/")
def cum_pl_long():
    """
    Chart for back test reports of Cumulative profit and loss for long strategy
    :return: None
    """
    if result.__contains__(ct.key_long) & (result.__contains__(ct.key_data_prop)):
        cum_long = result[ct.key_long][ct.key_date_cum_pl]
        data_properties = result[ct.key_data_prop]
        bt_chart = []
        for key, values in data_properties.items():
            bt_chart.append([key, values])
        return render_template("cum_pl_long.html", longData=cum_long, bt_chart_properties=bt_chart)


@app.route("/bt_report_short/")
def cum_pl_short():
    """
    Chart for back test reports of Cumulative profit and loss for short strategy
    :return: None
    """
    if result.__contains__(ct.key_short) & (result.__contains__(ct.key_data_prop)):
        cum_short = result[ct.key_short][ct.key_date_cum_pl]
        data_properties = result[ct.key_data_prop]
        bt_chart = []
        for key, values in data_properties.items():
            bt_chart.append([key, values])
        return render_template("cum_pl_short.html", shortData=cum_short, bt_chart_properties=bt_chart)
