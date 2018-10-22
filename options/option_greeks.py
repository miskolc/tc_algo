from datetime import date

from QuantLib import *

from constants import Keys
from options import greeks_calculator

success = 0
failure = 0


# maturity_date = Date(25, 10, 2018)
# spot_price = 10314
# strike_price = 10400
# volatility = 0.0  # the historical vols for a year
# dividend_rate = 0
# option_type = Option.Call
# risk_free_rate = 0.0
# day_count = Actual365Fixed()
# calendar = India()
# calculation_date = Date(19, 10, 2018)
# Settings.instance().evaluationDate = calculation_date
#
# payoff = PlainVanillaPayoff(option_type, strike_price)
# exercise = EuropeanExercise(maturity_date)
# # european_option = VanillaOption(payoff, exercise)
# european_option = EuropeanOption(payoff, exercise)
#
# spot_handle = QuoteHandle(SimpleQuote(spot_price))
# flat_ts = YieldTermStructureHandle(FlatForward(calculation_date, risk_free_rate, day_count))
# # dividend_yield = YieldTermStructureHandle(FlatForward(calculation_date, dividend_rate, day_count))
# flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, volatility, day_count))
# # bsm_process = BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
# bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)
#
# option_price = 54.20
# vol = european_option.impliedVolatility(targetValue=option_price, process=bs_process)
# print("Option Price: %s" % option_price)
# print("Vol: %s" % vol)
#
# flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, vol, day_count))
# bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)
#
# european_option.setPricingEngine(AnalyticEuropeanEngine(bs_process))
# bs_price = european_option.NPV()
# print("The theoretical price is %lf" % bs_price)
# print("Theta: %s" % european_option.theta())
# print("Theta per day: %s" % european_option.thetaPerDay())
# print("Gamma: %s" % european_option.gamma())
# print("Delta: %s" % european_option.delta())
# print("Vega: %s" % european_option.vega())

# ========================================================
# x = greeks_calculator.implied_vol(spot_price, strike_price, risk_free_rate, datetime.date(2018, 10, 25), 2.65)
# print("Vol---%s" % x)
# y=greeks_calculator.option_price(spot_price, strike_price, risk_free_rate *100, datetime.date(2018,10,25), x)
# print("Price: %s" % y.call)
# print("Theta: %s" % y.call_theta)
# print("Gamma: %s" % y.gamma)
# print("Vega: %s" % y.vega)


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

    # iv, theta, gamma, delta, vega = 0, 0, 0, 0, 0
    # if volatility == 00.01:
    #     iv = european_option.impliedVolatility(targetValue=option_price, process=bs_process)
    #
    #     flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, iv, day_count))
    #     bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)
    #
    #     # european_option.setPricingEngine(AnalyticEuropeanEngine(bs_process))
    #     # # bs_price = european_option.NPV()
    #     # theta = european_option.thetaPerDay()
    #     # gamma = european_option.gamma()
    #     # delta = european_option.delta()
    #     # vega = european_option.vega()
    # else:
    #     iv = volatility
    # print(spot_price, strike_price, expiry_date, option_type, option_price)
    # print(maturity_date)
    # print(calculation_date)
    # iv = european_option.impliedVolatility(targetValue=option_price, process=bs_process, )

    # print(spot_price, strike_price, expiry_date, option_type, option_price, calculation_date)
    # iv = european_option.impliedVolatility(targetValue=option_price, process=bs_process, )

    # global success, failure
    try:
        iv = european_option.impliedVolatility(targetValue=option_price, process=bs_process, minVol=0.001, maxVol=1000,
                                               maxEvaluations=1000000)
        iv = iv * 100
        flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, iv, day_count))
        bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)

        european_option.setPricingEngine(AnalyticEuropeanEngine(bs_process))
        # bs_price = european_option.NPV()
        theta = european_option.thetaPerDay()
        gamma = european_option.gamma()
        delta = european_option.delta()
        vega = european_option.vega()
        # success += 1
        # flat_vol_ts = BlackVolTermStructureHandle(BlackConstantVol(calculation_date, calendar, iv, day_count))
        # bs_process = BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)
    except RuntimeError:
        iv = 'NA'
        # failure += 1
        # print(e)
        # print(spot_price, strike_price, expiry_date, option_type, option_price, calculation_date)
        theta = 'NA'
        gamma = 'NA'
        delta = 'NA'
        vega = 'NA'

    return iv, theta, gamma, delta, vega
# ==============================================================
# exercise = EuropeanExercise(Date(25, October, 2018))
# payoff = PlainVanillaPayoff(Option.Call, 100.0)
# option = EuropeanOption(payoff, exercise)
# calculation_date = Date(20, 10, 2018)
# Settings.instance().evaluationDate = calculation_date

# S = QuoteHandle(SimpleQuote(100.0))  # Spot Price
# r = YieldTermStructureHandle(FlatForward(0, TARGET(), 0.03, Actual360()))  # Interest rate
# q = YieldTermStructureHandle(FlatForward(0, TARGET(), 0.01, Actual360()))  # Dividend yields
# sigma = BlackVolTermStructureHandle(BlackConstantVol(0, TARGET(), 0.20, Actual360()))
# process = BlackScholesProcess(S, r, sigma)

# option.impliedVolatility(11.10, process)

# engine = AnalyticEuropeanEngine(process)
# option.setPricingEngine(engine)
# option.NPV()
