import logging
from datetime import date

import options as op

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    op.data_insertion.insert_bulk_data(path='C:/Users/sb/Downloads/niftyoptionsdata/')
    # op.data_insertion.insert_bhavcopy("C:/Users/sb/Downloads/niftyoptionsdata/", "23OCT2018.zip")
    # op.data_insertion.update_option_greeks(date(2018,10,23))
    op.data_insertion.update_option_greeks()
