import logging
from datetime import date

import mibian

from model import GreekValues

_logger = logging.getLogger("greeks_calculator")

"""
Definitions written in this file are based on the mibian library for greeks calculation.
"""


def days_to_expiry(expiry_date: date, obs_date: date = None):
    """
    It returns the number of days left for the expiry from the date of observation.
    :param expiry_date: date
                Expiry date
    :param obs_date: date
                Observation date. By default the current date.
    :return: int
                Number of days to expiry
    """
    if obs_date is None:
        delta = expiry_date - date.today()
    else:
        delta = expiry_date - obs_date
    # print(delta.days)
    return delta.days


def option_price(underlying_price: float, strike_price: float, interest: float, expiry_date: date,
                 volatility: float, obs_date: date = None):
    """
    It is used to evaluate option's theoretical price and it's related greeks.
    :param underlying_price: float
                (S) Spot price
    :param strike_price: float
                (K) Strike price
    :param interest: float
                (r) Risk free interest rate
    :param expiry_date: date
                (T) Time to maturity i.e. expiry date
    :param volatility: float
                (v) (sigma) Volatility of the option
    :param obs_date: date
                Date of observation. By default present date.
    :return: GreekValues
    """
    # BS([underlyingPrice, strikePrice, interestRate, daysToExpiration], volatility=x, callPrice=y, putPrice=z)
    days_to_exp = days_to_expiry(expiry_date, obs_date)
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
                obs_date: date = None, call_price: float = None, put_price: float = None):
    """
    It is used to find the implied volatility of the option.
    Either call_price or put_price should be given.
    If both are given then call is evaluated by default.
    :param underlying_price: float
                (S) Spot price
    :param strike_price: float
                (K) Strike price
    :param interest: float
                (r) Risk free interest rate
    :param expiry_date: date
                (T) Time to maturity i.e. expiry date
    :param obs_date: date
                Date of observation. By default present date.
    :param call_price: float
                Call option price for the strike.
    :param put_price: float
                Put option price for the strike.
    :return: float
                Implied volatility of the option
    """
    days_expiry = days_to_expiry(expiry_date, obs_date=obs_date)
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
            # if iv == float("1e-05"):
            #     iv = 0.00001
            return iv
    else:
        _logger.warning("Enter a date greater than today")
        _logger.info("You entered: %s" % expiry_date)
        return


def put_call_parity(underlying_price: float, strike_price: float, interest: float, expiry_date: date,
                    obs_date: date = None, call_price: float = None, put_price: float = None):
    """
    This is used to find the put call parity for the options.
    Both call and put option price are required.
    :param underlying_price: float
                (S) Spot price
    :param strike_price: float
                (K) Strike price
    :param interest: float
                (r) Risk free interest rate
    :param expiry_date: date
                (T) Time to maturity i.e. expiry date
    :param obs_date: date
                Date of observation. By default present date.
    :param call_price: float
                Call option price for the strike.
    :param put_price: float
                Put option price for the strike.
    :return: tuple(float, float)
                Returns put call parity and implied volatility
    """
    days_expiry = days_to_expiry(expiry_date, obs_date=obs_date)
    if days_expiry > 0:
        if (call_price is None) & (put_price is None):
            _logger.warning("Both call and put price need to be given")
        else:
            c = mibian.BS([underlying_price, strike_price, interest, days_expiry], callPrice=call_price,
                          putPrice=put_price)
            return c.putCallParity, c.impliedVolatility
    else:
        _logger.warning("Enter a date greater than today")
        _logger.info("You entered: %s" % expiry_date)
        return
