from flask import Flask, render_template
from constants import Keys

"""
List of Charts:
1. Chart with indicators
2. BackTest with Annotation (Buy and Sell)
3. BackTest Report - Cum P&L all
                   - Cum P&L Long
                   - Cum P&L Short
"""

result = {}
app = Flask(__name__)


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
    if (result.__contains__(Keys.data_prop)) & (result.__contains__(Keys.data)) & (
            result.__contains__(Keys.params)):
        data_properties = result[Keys.data_prop]
        main_chart = []
        for key, values in data_properties.items():
            main_chart.append([key, values])
        params = result[Keys.params]
        data_list = result[Keys.data]
        return render_template("chart.html", chartData=data_list, chart_params=params, main_chart_properties=main_chart)
    else:
        return render_template("404.html")


@app.route("/backtest/")
def back_test_template():
    """
    For plotting back test chart with annotations.
    :return: None
    """
    if (result.__contains__(Keys.data_prop)) & (result.__contains__(Keys.data)) & (
            result.__contains__(Keys.params)) & (result.__contains__(Keys.annotations)):
        data_properties = result[Keys.data_prop]
        main_chart = []
        for key, values in data_properties.items():
            main_chart.append([key, values])
        params = result[Keys.params]
        data_list = result[Keys.data]
        annotations = result[Keys.annotations]
        return render_template("backtest.html", chartData=data_list, chart_params=params,
                               main_chart_properties=main_chart, chart_annotations=annotations)
    else:
        return render_template("404.html")


@app.route("/bt_report_all/")
def cum_pl_all():
    """
    Chart for back test reports of Cumulative profit and loss for all strategies
    :return: None
    """
    if result.__contains__(Keys.all) & (result.__contains__(Keys.data_prop)):
        cum_all = result[Keys.all][Keys.date_cum_pl]
        data_properties = result[Keys.data_prop]
        bt_chart = []
        for key, values in data_properties.items():
            bt_chart.append([key, values])
        return render_template("cum_pl_all.html", chartData=cum_all, bt_chart_properties=bt_chart)
    else:
        return render_template("404.html")


@app.route("/bt_report_long/")
def cum_pl_long():
    """
    Chart for back test reports of Cumulative profit and loss for long strategy
    :return: None
    """
    if result.__contains__(Keys.long) & (result.__contains__(Keys.data_prop)):
        cum_long = result[Keys.long][Keys.date_cum_pl]
        data_properties = result[Keys.data_prop]
        bt_chart = []
        for key, values in data_properties.items():
            bt_chart.append([key, values])
        return render_template("cum_pl_long.html", longData=cum_long, bt_chart_properties=bt_chart)
    else:
        return render_template("404.html")


@app.route("/bt_report_short/")
def cum_pl_short():
    """
    Chart for back test reports of Cumulative profit and loss for short strategy
    :return: None
    """
    if result.__contains__(Keys.short) & (result.__contains__(Keys.data_prop)):
        cum_short = result[Keys.short][Keys.date_cum_pl]
        data_properties = result[Keys.data_prop]
        bt_chart = []
        for key, values in data_properties.items():
            bt_chart.append([key, values])
        return render_template("cum_pl_short.html", shortData=cum_short, bt_chart_properties=bt_chart)
    else:
        return render_template("404.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
