from flask import Flask, render_template

import api
import data_parser
import indicators
import strategy
from strategy import Strategies
from model import *

app = Flask(__name__)


@app.route("/")
def backtestreport():
    data_prop, data = data_parser.get_data()
    high = data_parser.get_high(data)
    low = data_parser.get_low(data)
    close = data_parser.get_close(data)
    sma = indicators.sma(close)
    ema = indicators.ema(close)
    macd = indicators.macd(close)
    rsi = indicators.rsi(close)
    stoch = indicators.stoch(high, low, close)
    bbands = indicators.bollinger_bands(close)
    pivot = indicators.pivot(data)
    chart_1 = ChartElement(data=sma, label="sma", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.YELLOW)
    chart_2 = ChartElement(data=ema, label="ema", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.PINK)
    chart_3 = ChartElement(data=stoch, label="stoch", chart_type=ChartType.LINE, plot=ChartAxis.DIFFERENT_AXIS,
                           color=ChartColor.PURPLE)
    chart_4 = ChartElement(data=bbands, label="bbands", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.BLUE)
    chart_5 = ChartElement(data=pivot, label="pivot", chart_type=ChartType.LINE, plot=ChartAxis.SAME_AXIS,
                           color=ChartColor.GREEN)
    chart_6 = ChartElement(data=rsi, label="rsi", chart_type=ChartType.LINE, plot=1,
                           color=ChartColor.RED)
    chart_7 = ChartElement(data=macd, label="macd", chart_type=ChartType.LINE, plot=2,
                           color="magenta")
    charts = [chart_1, chart_2, chart_3, chart_6]
    buy = Condition(data1=sma, data2=ema, operation=Operation.CROSSOVER)
    sell = Condition(data1=rsi, data2=70, operation=Operation.GREATER_THAN)
    result = strategy.strategy_builder(data_properties=data_prop, data_list=data, charts=charts, buy=buy, sell=sell,
                                       target=1.0, sl=0.5, strategy=strategy.BUY)

    cum_all = result['all']['DATE_CUM_PL']
    cum_long = result['long']['DATE_CUM_PL']
    cum_short = result['short']['DATE_CUM_PL']

    print(cum_long)

    # return render_template("cumall.html", chartData=cum_all)
    # return render_template("cumlong.html", longData=cum_long)
    return render_template("cumshort.html", shortData=cum_short)


if __name__ == "__main__":
    app.run()
