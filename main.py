import logging
import numpy

import indicators


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    close = numpy.random.random(105) * 20
    indicators.sma(close, 25)
    # indicators.ema(close, 20)
    # indicators.indicator_info("ema")


