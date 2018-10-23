import numpy as np
import scipy.stats as si
import sympy as sy
from options import greeks_calculator, data_insertion, option_greeks, database_connection


def euro_vanilla(spot, strike, time_to_maturity, int_rate, vol, option='call'):
    # S: spot price
    # K: strike price
    # T: time to maturity
    # r: interest rate
    # sigma: volatility of underlying asset

    d1 = (np.log(spot / strike) + (int_rate + 0.5 * vol ** 2) * time_to_maturity) / (vol * np.sqrt(time_to_maturity))
    d2 = (np.log(spot / strike) + (int_rate - 0.5 * vol ** 2) * time_to_maturity) / (vol * np.sqrt(time_to_maturity))

    if option == 'call':
        result = (spot * si.norm.cdf(d1, 0.0, 1.0) - strike * np.exp(-int_rate * time_to_maturity) * si.norm.cdf(d2,
                                                                                                                 0.0,
                                                                                                                 1.0))
    elif option == 'put':
        result = (strike * np.exp(-int_rate * time_to_maturity) * si.norm.cdf(-d2, 0.0, 1.0) - spot * si.norm.cdf(-d1,
                                                                                                                  0.0,
                                                                                                                  1.0))
    else:
        result = None
    return result
