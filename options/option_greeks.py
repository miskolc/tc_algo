from datetime import date

from QuantLib import *

from constants import Keys

success = 0
failure = 0


def get_greeks(spot_price, strike_price, expiry_date: date, option_type: str, option_price: float,
               calculation_date: date = None, volatility: float = None):
    maturity_date = Date(expiry_date.day, expiry_date.month, expiry_date.year)
    # volatility = 0.0  # the historical vols for a year
    # print(spot_price, strike_price, expiry_date, option_type, option_price, calculation_date)

    option = Option.Call
    if option_type == Keys.call:
        option = Option.Call
    if option_type == Keys.put:
        option = Option.Put
    risk_free_rate = 0.0
    day_count = Actual365Fixed()
    calendar = India()
    if calculation_date is not None:
        calculation_date = Date(calculation_date.day, calculation_date.month, calculation_date.year)
        Settings.instance().evaluationDate = calculation_date

    payoff = PlainVanillaPayoff(option, strike_price)
    exercise = EuropeanExercise(maturity_date)
    european_option = EuropeanOption(payoff, exercise)

    spot_handle = QuoteHandle(SimpleQuote(spot_price))
    flat_ts = YieldTermStructureHandle(FlatForward(calculation_date, risk_free_rate, day_count))
    flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, volatility, day_count))
    bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)

    try:
        iv = european_option.impliedVolatility(targetValue=option_price, process=bs_process, minVol=0.001, maxVol=1000,
                                               maxEvaluations=1000000)
        # iv = iv * 100
        flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, iv, day_count))
        bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)

        european_option.setPricingEngine(AnalyticEuropeanEngine(bs_process))
        # bs_price = european_option.NPV()
        iv = iv * 100
        theta = european_option.thetaPerDay()
        gamma = european_option.gamma()
        delta = european_option.delta()
        vega = european_option.vega()
        # rho = european_option.rho()

    except RuntimeError:
        iv = "''"
        theta = "''"
        gamma = "''"
        delta = "''"
        vega = "''"
        # rho = "''"

    return iv, theta, gamma, delta, vega,


def get_option_greeks(spot_price, strike_price, expiry_date: date, option_type: str, option_price: float,
                      calculation_date: date = None, implied_vol: float = None):
    maturity_date = Date(expiry_date.day, expiry_date.month, expiry_date.year)
    # volatility = 0.0  # the historical vols for a year
    # print(spot_price, strike_price, expiry_date, option_type, option_price, calculation_date)

    option = Option.Call
    if option_type == Keys.call:
        option = Option.Call
    if option_type == Keys.put:
        option = Option.Put
    risk_free_rate = 0.0
    day_count = Actual365Fixed()
    calendar = India()
    if calculation_date is not None:
        calculation_date = Date(calculation_date.day, calculation_date.month, calculation_date.year)
        Settings.instance().evaluationDate = calculation_date

    payoff = PlainVanillaPayoff(option, strike_price)
    exercise = EuropeanExercise(maturity_date)
    european_option = EuropeanOption(payoff, exercise)

    spot_handle = QuoteHandle(SimpleQuote(spot_price))
    flat_ts = YieldTermStructureHandle(FlatForward(calculation_date, risk_free_rate, day_count))
    flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, implied_vol, day_count))
    bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)

    european_option.setPricingEngine(AnalyticEuropeanEngine(bs_process))

    delta = european_option.delta()
    gamma = european_option.gamma()
    theta = european_option.thetaPerDay()
    vega = european_option.vega()
    rho = european_option.rho()

    return delta, gamma, theta, vega, rho
