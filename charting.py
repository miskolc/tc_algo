from flask import Flask, render_template
import data_parser
from strategy import Strategies

app = Flask(__name__)


@app.route("/")
def main():
    prop, data = data_parser.get_data(start_date="2017-08-18")
    result = Strategies.rsi(data, data_properties=prop)
    data_properties = result['data_properties']
    main_chart = []
    for key, values in data_properties.items():
        main_chart.append([key, values])
    params = result['params']
    data = result['data']

    # print(params,data_with_indicators)
    # final_data = data_with_indicators[1:]
    # print(final_data)

    return render_template("index.html", title="Anychart Python template", chartData=data, chart_params=params,
                           main_chart_properties=main_chart)


if __name__ == "__main__":
    app.run()
