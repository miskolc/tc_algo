import logging
from datetime import date

import matplotlib.pyplot as plt
import numpy
import plotly.offline as py
import plotly.tools as tls

from constants import Keys
from options import option_greeks

_logger = logging.getLogger("payoff_charts")


def _get_payoff_values(spot, strike: int, option_type: str, premium: float):
    """
    It evaluates the payoff values of the option
    :param spot: list
            Underlying Values for which evaluation is required
    :param strike: int
            Strike of the option
    :param option_type: str
            Type of the option. Possible values: CE and PE
    :param premium: float
            Option premium price.
    :return: list
            Contains payoff values corresponding to the spot vales
    """
    payoff = []
    for underlying in spot:
        value = (max(0, (underlying - strike) if option_type == Keys.call else (strike - underlying))) - premium
        payoff.append(value)
    return payoff


def _get_greeks_payoff_values(spot, strike: int, expiry_date: date, calculation_date: date, option_type: str,
                              volatility: float):
    """
    It evaluates the greeks payoff values of the option
    :param spot: list
            Underlying Values for which evaluation is required
    :param strike: int
            Strike of the option
    :param expiry_date: date
            Date of expiry of option
    :param calculation_date: date
            Observation date for the calculations
    :param option_type: str
            Type of the option. Possible values: CE and PE
    :param volatility: float
            Volatility for the option
    :return: tuple(list, list, list, list, list)
            Returns values for delta, gamma, theta, vega, rho for corresponding spot in list
    """
    delta_list, gamma_list, theta_list, vega_list, rho_list = [], [], [], [], []

    for underlying in spot:
        # print(underlying)
        delta, gamma, theta, vega, rho = option_greeks.get_option_greeks(underlying, strike, expiry_date,
                                                                         option_type, volatility, calculation_date, )
        delta_list.append(delta)
        gamma_list.append(gamma)
        theta_list.append(theta)
        vega_list.append(vega)
        rho_list.append(rho)

    return delta_list, gamma_list, theta_list, vega_list, rho_list


def payoff_charts(spot: list, strike: int, option_type: str, option_price: float, calculation_date: date,
                  expiry_date: date, volatility: float):
    """
    It is used to display the payoff charts for the input option data
    :param spot: list
            Underlying Values for which evaluation is required
    :param strike: int
            Strike of the option
    :param option_type: str
            Type of the option. Possible values: CE and PE
    :param option_price: float
            Option premium price.
    :param calculation_date: date
            Observation date for the calculations
    :param expiry_date: date
            Date of expiry of option
    :param volatility: float
            Volatility for the option
    :return: None
            Displays payoff charts in the browser.
    """
    spot = numpy.arange(min(spot), max(spot), 100, dtype=numpy.int64).tolist()

    if option_type in [Keys.call, Keys.put]:
        payoff_list = _get_payoff_values(spot, strike, option_type, option_price)
        delta_list, gamma_list, theta_list, vega_list, rho_list = _get_greeks_payoff_values(spot, strike, expiry_date,
                                                                                            calculation_date,
                                                                                            option_type,
                                                                                            volatility)

        fig = plt.figure()

        if payoff_list is not None:
            ax6 = fig.add_subplot(321)
            ax6.plot(spot, payoff_list, )
            ax6.set_title('Payoff')

        if delta_list:
            ax1 = fig.add_subplot(322)
            ax1.plot(spot, delta_list, )
            ax1.set_title('Delta')

            ax2 = fig.add_subplot(323)
            ax2.plot(spot, gamma_list, )
            ax2.set_title('Gamma')

            ax3 = fig.add_subplot(324)
            ax3.plot(spot, theta_list, )
            ax3.set_title('Theta')

            ax4 = fig.add_subplot(325)
            ax4.plot(spot, vega_list, )
            ax4.set_title('Vega')

            ax5 = fig.add_subplot(326)
            ax5.plot(spot, rho_list, )
            ax5.set_title('Rho')

        plt.tight_layout()
        fig = plt.gcf()

        name = '%s %s %s' % (
            strike, option_type, expiry_date.strftime("%d%b%Y"))

        plotly_fig = tls.mpl_to_plotly(fig)
        plotly_fig['layout']['title'] = 'Greeks Payoff Charts for %s' % name
        plotly_fig['layout']['margin'].update({'t': 80})
        plotly_fig['layout']['height'] = 720
        plotly_fig['layout']['width'] = 1024

        py.plot(plotly_fig, filename="%s.html" % name)

    else:
        _logger.warning("Option can be either CE or PE")
        _logger.info("Couldn't plot payoffs")

# if __name__ == '__main__':
#     payoff_charts([9000, 11100], 10000, Keys.put, 276., date(2018, 10, 26), date(2018, 11, 29), 20.95)
