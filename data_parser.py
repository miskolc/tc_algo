import logging
from datetime import *

import numpy
import quandl

import api
from model import *

_logger = logging.getLogger("data_parser")
br = "^"


def get_date_ohlc(symbol: str = api.nifty50, start_date: str = api.start_date, end_date: str = "") -> dict:
    """
    This is used when data is required in separate list
    :param symbol: str
                Scrip for which data is required
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
    date_ohlc = {"symbol": symbol, "date": date_values, "open": open, "high": high, "low": low, "close": close,
                 "volume": volume}
    return date_ohlc


def get_data(symbol: str = api.nifty50, start_date: str = api.start_date, end_date: str = "") -> tuple:
    """
    This is base function which extracts data from Quandl in a DataObject
    :param symbol: str
                Scrip for which data is required
    :param start_date: str
                Starting date for data. For e.g. '2017-08-08'
    :param end_date: str
                End date for data. For e.g. '2018-08-08'
    :return: tuple
            data_properties: dict
                        Contains info about the data fetched from Quandl API. Such as scrip, start date etc.
            data: list[DataObject]
    """
    data = []
    quandl.ApiConfig.api_key = api.quandl_api_key
    response = quandl.get(symbol, returns="numpy", start_date=start_date, end_date=end_date)
    for i in range(len(response)):
        item = response[i]
        data.append(DataObject(item))
    # _logger.debug("%s" % data)
    scrip = symbol.split("/")
    data_properties = dict(scrip=scrip[1], start_date=start_date, end_date=end_date, chart="%s" % ChartType.CANDLESTICK)
    return data_properties, data


def get_ohlc(data: list = None) -> tuple:
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
    # date_arr = date_format(date_arr)
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
    # date1 = date(year=2018, month=1, day=15)
    # delta = relativedelta.relativedelta(month=1)
    # old = current - delta
    # test = date(year=2018, month=7, day=15)
    # print(date2 < test < date1)
    return current


def data_builder(data: list, data_properties: dict, charts: list = None) -> tuple:
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
    params = ["date", "open", "high", "low", "close", "volume"]
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
    # result = [params]
    # for item in father:
    #     result.append(item)
    # return result


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
            child.volume = 'null'
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
            # if type(item[i]) == PivotObject:
            #     pv = item[i]
            #     item[i] = [pv.pp, pv.r1, pv.r2, pv.r3, pv.s1, pv.s2, pv.s3]
            #     father[i] += item[i]
            # else:
            father[i].append(item[i])
    return father
