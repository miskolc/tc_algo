import json
import logging
import os
from datetime import date
from typing import Union

from data.common import ApiKey, ExitCode as ec
import quandl
import pandas

logger = logging.getLogger("data")


class QuandlSymbol(object):

    def __init__(self, scrip: str, source: str = 'NSE', column_index: Union[int, list] = None):
        # column_index (NSE-Index)-> 0=Index,1=Open,2=High,3=Low,4=Close,5=Volume,6=Turnover
        # column_index (NSE-EQ)-> 0=Index,1=Open,2=High,3=Low,4=Last,5=Close,6=Volume,7=Turnover
        symbol = source + "/" + scrip
        self.api_symbol = symbol
        self.symbol = []
        if column_index:
            if isinstance(column_index, int):
                column_index = [column_index]
            if isinstance(column_index, list):
                for index in column_index:
                    if isinstance(index, int):
                        self.symbol.append(symbol + "." + str(index))
        else:
            self.symbol = [symbol]

    def __str__(self) -> str:
        return repr(self.symbol)


class QuandlTimeSeries(object):
    config_key = "quandl_key"
    date_fmt = "%Y-%m-%d"
    attempts = 5

    def __init__(self, dataset: Union[str, list], start_date: date = None, end_date: date = None, interval=None,
                 transform=None, rows: int = None, data_csv: str = None, quandl_key: str = None,
                 clear_token: bool = False):
        self.filename = 'config.json'
        if clear_token:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
        if quandl_key:
            self.key = quandl_key
        else:
            self.key = self.__get_key()
        quandl.api_config.ApiConfig = self.key
        if isinstance(dataset, (list, QuandlSymbol)):
            scrips = []
            dataset = [dataset] if isinstance(dataset, QuandlSymbol) else dataset
            for _scrip in dataset:
                if isinstance(_scrip, str):
                    scrips.append(_scrip)
                if isinstance(_scrip, QuandlSymbol):
                    scrips += _scrip.symbol

            self.api_data = scrips[0] if len(scrips) == 1 else scrips
        if isinstance(dataset, str):
            self.api_data = dataset
        self.start_date = start_date.strftime(self.date_fmt) if start_date else None
        self.end_date = end_date.strftime(self.date_fmt) if end_date else None
        self.interval = interval if interval in ApiKey.quandl_intervals else None
        self.transform = transform if transform in ApiKey.quandl_transform else None
        self.data = quandl.get(self.api_data, start_date=self.start_date, end_date=self.end_date,
                               collapse=self.interval, transform=self.transform, rows=rows)
        self.columns = self.data.columns
        if data_csv:
            self.data.to_csv(data_csv)

    def get_value(self, key):
        if key in self.columns:
            return self.data[key].values
        else:
            print("Invalid Key")
            print(f"Available columns are: {self.columns}")

    def __check_key(self):
        try:
            f = open(self.filename, 'r')
            json.load(f)
            f.close()
        except (IOError, json.decoder.JSONDecodeError):
            logger.debug("No file or invalid file structure")
            default_data = {self.config_key: ""}
            with open(self.filename, 'w') as output_file:
                json.dump(default_data, output_file)
        return True

    def __get_key(self):
        if self.__check_key() and QuandlTimeSeries.attempts > 0:
            file = open(self.filename, 'r')
            try:
                data = json.load(file)
                key = data[self.config_key]
                if key:
                    return key
                else:
                    print("API Key for quandl package not found. Please enter a key to continue.")
                    key = input("Key: ")
                    if key:
                        data[self.config_key] = key
                        with open(self.filename, 'w') as output_file:
                            json.dump(data, output_file)
                        return key
                    else:
                        QuandlTimeSeries.attempts -= 1
                        print("Retry with valid entry...")
                        self.__get_key()
            except KeyError:
                logger.warning(f"Error in key: {self.key}")
                pass
            finally:
                file.close()
            return None
        else:
            logger.warning("Max Attempts")
            exit(ec.max_attempts)


if __name__ == '__main__':
    nifty = QuandlSymbol(scrip='CNX_NIFTY', column_index=4)
    hdfcbank = QuandlSymbol(scrip='HDFCBANK', column_index=5)
    yesbank = QuandlSymbol(scrip='YESBANK', column_index=5)
    # series_data = QuandlTimeSeries('nse/cnx_nifty.4', )
    series_data = QuandlTimeSeries([nifty])
    # print(series_data.data)
    # print(series_data.columns)
    close = series_data.get_value('Close')
    print(close)
