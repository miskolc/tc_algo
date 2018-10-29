import logging
from datetime import date

import options as op

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # op.data_insertion.insert_bulk_data(path='C:/Users/sb/Downloads/niftyoptionsdata/')
    # op.data_insertion.insert_bhavcopy("C:/Users/sb/Downloads/niftyoptionsdata/", "26OCT2018.zip")
    # op.data_insertion.update_option_greeks(date(2018, 10, 26))
    # op.data_insertion.update_option_greeks()
    # app = op.market_watch.get_market_watch_app()
    # app.run_server()
