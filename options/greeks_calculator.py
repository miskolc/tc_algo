import logging

import mibian
from dateutil import relativedelta
from datetime import date, timedelta

from model import GreekValues

_logger = logging.getLogger("greeks_calculator")


def days_to_expiry(expiry_date: date, obs_date: date = None):
    if obs_date is None:
        delta = expiry_date - date.today()
    else:
        delta = expiry_date - obs_date
    # print(delta.days)
    return delta.days


def option_price(underlying_price: float, strike_price: float, interest: float, expiry_date: date,
                 volatility: float, obs_data: date = None):
    # BS([underlyingPrice, strikePrice, interestRate, daysToExpiration], volatility=x, callPrice=y, putPrice=z)
    days_to_exp = days_to_expiry(expiry_date, obs_data)
    if days_to_exp > 0:
        c = mibian.BS([underlying_price, strike_price, interest, days_to_exp], volatility=volatility)
        call = c.callPrice
        call_delta = c.callDelta
        call_dual_delta = c.callDelta2
        call_theta = c.callTheta
        call_rho = c.callRho

        put = c.putPrice
        put_delta = c.putDelta
        put_dual_delta = c.putDelta2
        put_theta = c.putTheta
        put_rho = c.putRho

        vega = c.vega
        gamma = c.gamma
        greek_values = GreekValues(call, call_delta, call_dual_delta, call_theta, call_rho, put, put_delta,
                                   put_dual_delta, put_theta, put_rho, vega, gamma)
        return greek_values
    elif days_to_exp == 0:
        greek_values = GreekValues(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        return greek_values
    else:
        _logger.warning("Enter a date greater than today")
        _logger.info("You entered: %s" % expiry_date)
        greek_values = GreekValues(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        return greek_values


def implied_vol(underlying_price: float, strike_price: float, interest: float, expiry_date: date,
                timestamp: date = None, call_price: float = None, put_price: float = None):
    days_expiry = days_to_expiry(expiry_date, obs_date=timestamp)
    if days_expiry > 0:
        if (call_price is None) & (put_price is None):
            _logger.warning("Either call or put price need to be given")
        else:
            c = mibian.BS
            if call_price is not None:
                c = mibian.BS([underlying_price, strike_price, interest, days_expiry], callPrice=call_price)
            elif put_price is not None:
                c = mibian.BS([underlying_price, strike_price, interest, days_expiry], putPrice=put_price)
            iv = c.impliedVolatility
            if iv == float("1e-05"):
                iv = 0.00001
            return iv
    else:
        _logger.warning("Enter a date greater than today")
        _logger.info("You entered: %s" % expiry_date)
        return


def put_call_parity(underlying_price: float, strike_price: float, interest: float, expiry_date: date,
                    call_price: float = None, put_price: float = None):
    days_expiry = days_to_expiry(expiry_date)
    if days_expiry > 0:
        if (call_price is None) & (put_price is None):
            _logger.warning("Either call or put price need to be given")
        else:
            c = mibian.BS([underlying_price, strike_price, interest, days_expiry], callPrice=call_price,
                          putPrice=put_price)
            return c.putCallParity, c.impliedVolatility
    else:
        _logger.warning("Enter a date greater than today")
        _logger.info("You entered: %s" % expiry_date)
        return
