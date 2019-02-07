import logging
import os
import zipfile
from datetime import datetime

import pandas as pd
from requests import Session


class Bhavcopy(object):
    """
    This class only downloads NSE Bhavcopy for Equities and Derivatives
    """
    headers = {
        'Host': 'www.nseindia.com',
        'Referer': 'https://www.nseindia.com/products/content/derivatives/equities/archieve_fo.htm'
    }
    fo_bhavcopy = 'https://www.nseindia.com/content/historical/DERIVATIVES/{year}/{month}/fo{day}{month}{' \
                  'year}bhav.csv.zip'
    cm_bhavcopy = 'https://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day}{month}{year}bhav.csv.zip'
    YEAR = '%Y'
    MONTH = '%b'
    DAY = '%d'

    def __init__(self, obs_date: datetime = None, cm: bool = False):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.obs_date = obs_date if obs_date else datetime.now()
        year = self.obs_date.strftime(self.YEAR)
        month = self.obs_date.strftime(self.MONTH).upper()
        day = self.obs_date.strftime(self.DAY)
        self.cm = cm
        if cm:
            self.bhavcopy_url = self.cm_bhavcopy.format(year=year, month=month, day=day)
        else:
            self.bhavcopy_url = self.fo_bhavcopy.format(year=year, month=month, day=day)
        self.logger.debug(self.bhavcopy_url)

    def get(self, overwrite: bool = False):
        self.__check_dir()
        _download = not self.__check_file()
        _download = True if overwrite else _download
        if _download:
            self.__download()
        else:
            self.logger.info(f"Using cached file {self.__extracted_file} for reading")

        try:
            df = pd.read_csv(self.__extracted_file)
            return df
        except FileNotFoundError:
            self.logger.warning(f"Either invalid date or corrupted file was supplied.\nDate fetched: {self.obs_date}")
            return

    def __download(self, ):
        session = Session()
        session.headers.update(self.headers)
        r = session.get(self.bhavcopy_url, )
        if r.ok:
            zipped_bytes = r.content
            with open(self.__compressed_file, 'wb') as out_file:
                out_file.write(zipped_bytes)
            zf = zipfile.ZipFile(file=self.__compressed_file, mode='r')
            zf.extractall(self.__extracted)
            df = pd.read_csv(self.__extracted_file)
            if self.cm:
                del df['Unnamed: 13']
            else:
                del df['Unnamed: 15']
            df.to_csv(self.__extracted_file, index=False)
        else:
            self.logger.info(f"Unable to download bhavcopy for {self.obs_date}")

    def __check_dir(self):
        self.__downloads = './downloads/'
        self.__compressed = os.path.join(self.__downloads, 'compressed/')
        self.__extracted = os.path.join(self.__downloads, 'extracted/')
        os.makedirs(self.__compressed, exist_ok=True)
        os.makedirs(self.__extracted, exist_ok=True)

    def __check_file(self):
        filename = self.bhavcopy_url.split('/')[-1]
        self.__compressed_filename = filename.replace('.csv', '')
        self.__extracted_filename = filename.replace('.zip', '')
        self.__compressed_file = os.path.join(self.__compressed, self.__compressed_filename)
        self.__extracted_file = os.path.join(self.__extracted, self.__extracted_filename)
        self.logger.debug(f"Compressed File {self.__compressed_file}")
        if os.path.isfile(self.__compressed_file) and os.path.isfile(self.__extracted_file):
            return True
        else:
            return False
