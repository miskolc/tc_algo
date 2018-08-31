import calendar
import logging
from datetime import *

import quandl
from dateutil.relativedelta import relativedelta

import api
from api import *
from model import *

_logger = logging.getLogger("data_parser")


def get_date_ohlc(symbol: Symbol = NSEFO.NIFTY50, start_date: str = api.min_date, end_date: str = "") -> dict:
    """
    This is used when data is required in separate list
    :param symbol: Symbol
                Scrip for which data is required. An Instance of api.Symbol class
    :param start_date: str
                Starting date for data. For e.g. '2017-08-08'
    :param end_date: str
                End date for data. For e.g. '2018-08-08'
    :return: dict
            Data of the form: {"symbol": list, "date": list, "open": list, "high": list, "low": list, "close": list,
                 "volume": list}
    """
    data_prop, data = get_data(symbol=symbol, start_date=start_date, end_date=end_date)
    date_values = get_date(data)
    open = get_open(data)
    high = get_high(data)
    low = get_low(data)
    close = get_close(data)
    volume = get_volume(data)
    date_ohlc = {Keys.symbol: symbol.scrip,
                 Keys.date: date_values,
                 Keys.open: open,
                 Keys.high: high,
                 Keys.low: low,
                 Keys.close: close,
                 Keys.volume: volume}
    return date_ohlc


def get_data(symbol: Symbol = NSEFO.NIFTY50, start_date: str = api.min_date, end_date: str = "",
             interval: str = Keys.daily):
    """
    This is base function which extracts data from Quandl in a DataObject
    :param symbol: Symbol
                Scrip for which data is required. An Instance of api.Symbol class
    :param start_date: str
                Starting date for data. For e.g. '2017-08-08'
    :param end_date: str
                End date for data. For e.g. '2018-08-08'
    :param interval: str
                Data Interval for the scrip.
                Currently supports daily, weekly, monthly and yearly formats.
    :return: tuple
            data_properties: dict
                        Contains info about the data fetched from Quandl API. Such as scrip, start date etc.
            data: list[DataObject]
    """
    data = []
    quandl.ApiConfig.api_key = api.quandl_api_key
    response = quandl.get(symbol.api_key, returns="numpy", start_date=start_date, end_date=end_date)
    for i in range(len(response)):
        item = response[i]
        data.append(DataObject(item))
    data_properties = {Keys.scrip: symbol.scrip,
                       Keys.start_date: start_date,
                       Keys.end_date: end_date,
                       Keys.chart: "%s" % ChartType.CANDLESTICK,
                       Keys.size: symbol.size}

    if interval == Keys.daily:
        data_properties.update({Keys.interval: Keys.daily})
        return data_properties, data
    elif interval == Keys.weekly:
        data_properties.update({Keys.interval: Keys.weekly})
        data = get_weekly_data(data)
        return data_properties, data
    elif interval == Keys.monthly:
        data_properties.update({Keys.interval: Keys.monthly})
        data = get_monthly_data(data)
        return data_properties, data
    elif interval == Keys.yearly:
        data_properties.update({Keys.interval: Keys.yearly})
        data = get_yearly_data(data)
        return data_properties, data
    else:
        data_properties.update({Keys.interval: interval})
        return data_properties, data


def get_weekly_data(data: list):
    candle_dates = []
    data_arr = []
    week_delta = relativedelta(weeks=1)
    first_date = data[0].date
    last_date = data[-1].date
    while first_date < last_date:
        weekday = first_date.isocalendar()
        back_time = timedelta(days=weekday[2] - 1)
        forward_time = timedelta(days=6)
        week_first = first_date - back_time
        week_last = week_first + forward_time
        candle_dates.append([week_first, week_last])
        first_date = first_date + week_delta
    for dates in candle_dates:
        month_date, open, high, low, close, volume, turnover = [], [], [], [], [], [], []
        for i in range(len(data)):
            if dates[0] <= data[i].date <= dates[1]:
                month_date.append(data[i].date)
                open.append(data[i].open)
                high.append(data[i].high)
                low.append(data[i].low)
                close.append(data[i].close)
                volume.append(data[i].volume)
                turnover.append(data[i].turnover)
        # month_date = dates[0]
        month_date = month_date[0]
        open = open[0]
        high = max(high)
        low = min(low)
        close = close[-1]
        volume = sum(volume)
        turnover = sum(turnover)
        obj = DataObject(**{Keys.date: month_date, Keys.open: open, Keys.high: high, Keys.low: low, Keys.close: close,
                            Keys.volume: volume, Keys.turnover: turnover})
        data_arr.append(obj)
    return data_arr


def get_monthly_data(data: list):
    candle_dates = []
    data_arr = []
    month_delta = relativedelta(months=1)
    first_date = data[0].date
    last_date = data[-1].date
    while first_date < last_date:
        days = calendar.monthrange(first_date.year, first_date.month)[1]
        candle_dates.append([date(year=first_date.year, month=first_date.month, day=1),
                             date(year=first_date.year, month=first_date.month, day=days)])
        first_date = first_date + month_delta
    for dates in candle_dates:
        month_date, open, high, low, close, volume, turnover = [], [], [], [], [], [], []
        for i in range(len(data)):
            if dates[0] <= data[i].date <= dates[1]:
                month_date.append(data[i].date)
                open.append(data[i].open)
                high.append(data[i].high)
                low.append(data[i].low)
                close.append(data[i].close)
                volume.append(data[i].volume)
                turnover.append(data[i].turnover)
        # month_date = dates[0]
        month_date = month_date[0]
        open = open[0]
        high = max(high)
        low = min(low)
        close = close[-1]
        volume = sum(volume)
        turnover = sum(turnover)
        obj = DataObject(**{Keys.date: month_date, Keys.open: open, Keys.high: high, Keys.low: low, Keys.close: close,
                            Keys.volume: volume, Keys.turnover: turnover})
        data_arr.append(obj)
    return data_arr


def get_yearly_data(data: list):
    candle_dates = []
    data_arr = []
    year_delta = relativedelta(years=1)
    first_date = data[0].date
    last_date = data[-1].date
    while first_date < last_date:
        candle_dates.append([date(year=first_date.year, month=1, day=1),
                             date(year=first_date.year, month=12, day=31)])
        first_date = first_date + year_delta
    for dates in candle_dates:
        year_date, open, high, low, close, volume, turnover = [], [], [], [], [], [], []
        for i in range(len(data)):
            if dates[0] <= data[i].date <= dates[1]:
                year_date.append(data[i].date)
                open.append(data[i].open)
                high.append(data[i].high)
                low.append(data[i].low)
                close.append(data[i].close)
                volume.append(data[i].volume)
                turnover.append(data[i].turnover)
        # month_date = dates[0]
        year_date = year_date[0]
        open = open[0]
        high = max(high)
        low = min(low)
        close = close[-1]
        volume = sum(volume)
        turnover = sum(turnover)
        obj = DataObject(**{Keys.date: year_date, Keys.open: open, Keys.high: high, Keys.low: low, Keys.close: close,
                            Keys.volume: volume, Keys.turnover: turnover})
        data_arr.append(obj)
    return data_arr


def get_ohlc(data: list = None):
    """
    When data is required in ohlc in list. This required for the pattern hunter operations.
    :param data: list[DataObject]
    :return: tuple
        A tuple containing open, high, low, close with each element as list.
    """
    if (data is None) | (data == []) | (type(data[0]) != DataObject):
        _logger.warning("Invalid data type in get_ohlc \nExpected %s got %s instead" % (DataObject, type(data[0])))
    else:
        open = numpy.asarray(get_open(data))
        high = numpy.asarray(get_high(data))
        low = numpy.asarray(get_low(data))
        close = numpy.asarray(get_close(data))
        return open, high, low, close


def get_date(data: list = None) -> list:
    """
    Get date from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only date
    """
    date_arr = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.date
            date_arr.append(value)
    return date_arr


def get_open(data: list = None) -> list:
    """
    Get open from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only open
    """
    open = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.open
            open.append(value)
    return open


def get_high(data: list = None):
    """
    Get high from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only high
    """
    high = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.high
            high.append(value)
    return high


def get_low(data: list = None):
    """
    Get low from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only low
    """
    low = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.low
            low.append(value)
    return low


def get_close(data: list = None):
    """
    Get close from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only close
    """
    close = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.close
            close.append(value)
    return close


def get_volume(data: list = None):
    """
    Get volume from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only volume
    """
    volume = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.volume
            volume.append(value)
    return volume


def get_turnover(data: list = None):
    """
    Get turnover from the list[DataObject]
    :param data: list[DataObject]
    :return: list
            A list containing only turnover
    """
    turnover = []
    if (data is None) | (data == []):
        _logger.warning("Invalid data")
    else:
        for i in data:
            value = i.turnover
            turnover.append(value)
    return turnover


def current_month(timestamp=""):
    """
    Required when date is in UNIX timestamp
    :param timestamp: str
    :return: datetime.datetime object
    """
    current = date.fromtimestamp(float(timestamp))
    return current


def data_builder(data: list, data_properties: dict, charts: list = None):
    """
    Data builder is used to get data for charting.
    It formats data for charting of candle and indicators.
    :param data: list[DataObject]
    :param data_properties: dict
                Data properties returned from get_data function
    :param charts: list[ChartElement]
                A chart element contains data to be plotted on chart. For e.g. indicators
    :return: tuple
        A tuple of the form data_properties, params, data_list.
        data_properties: dict
                    All the properties related to the candle data
        params: list
                    All the properties related to the indicator or other than candle data
        data_list: list
                    A 2D list of data for charting
    """
    params = [Keys.date, Keys.open, Keys.high, Keys.low, Keys.close, Keys.volume]
    data_list = _append_data(data)
    indicators = []
    if charts is None:
        _logger.debug("No chart element specified")
    elif type(charts) == list:
        _logger.debug("Charts specified")
        for chart_element in charts:
            if type(chart_element) == ChartElement:
                parameter = "%s^%s^%s^%s" % (
                    chart_element.type, chart_element.axis, chart_element.color, chart_element.label)
                item = chart_element.data
                if type(item) == list:
                    _logger.debug("list")
                    params.append(parameter)
                    indicators.append(item)
                elif type(item) == dict:
                    _logger.debug('dict')
                    for key, value in item.items():
                        params.append("%s_%s" % (parameter, key))
                        indicators.append(value)
                else:
                    _logger.warning("Unknown data format or type")

    data_list = _append_indicators(indicators, data_list)
    _logger.debug("Params are: %s" % params)
    _logger.debug("Data properties: %s" % data_properties)
    return data_properties, params, data_list


def _append_data(data):
    """
    Helper function for data_builder.
    :param data: list[DataObject]
    :return: list
            A 2D list of candle data
    """
    result = []
    for child in data:
        if numpy.isnan(child.volume):
            child.volume = ct.default
        grand_child = ["%s-%s-%s 09:15:00" % (child.date.year, child.date.month, child.date.day), child.open,
                       child.high,
                       child.low, child.close, child.volume]
        result.append(grand_child)
    return result


def _append_indicators(indicators, father):
    """
    Helper function for data_builder
    :param indicators: list
                A list of  data for the indicators to be plotted on chart
    :param father: list
                Data for candle charting
    :return: list
                A 2D list of data
    """
    for item in indicators:
        _logger.debug("Item: %s " % len(item))
        _logger.debug("Father: %s" % len(father))
        for i in range(len(father)):
            father[i].append(item[i])
    return father


def round_float(number: float) -> float:
    return float(Decimal(number).quantize(PRECISION))
