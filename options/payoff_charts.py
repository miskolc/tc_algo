import logging
from datetime import date

import matplotlib.pyplot as plt
import numpy
import plotly.offline as py
import plotly.tools as tls

from constants import Keys
from options import option_greeks

_logger = logging.getLogger("payoff_charts")


def get_payoff_values(spot, strike: int, option_type: str, premium: float):
    payoff = []
    for underlying in spot:
        value = (max(0, (underlying - strike) if option_type == Keys.call else (strike - underlying))) - premium
        payoff.append(value)
    return payoff


def get_greeks_payoff_values(spot, strike: int, expiry_date: date, calculation_date: date, option_type: str,
                             option_price: float, volatility: float):
    delta_list, gamma_list, theta_list, vega_list, rho_list = [], [], [], [], []

    for underlying in spot:
        # print(underlying)
        delta, gamma, theta, vega, rho = option_greeks.get_option_greeks(underlying, strike, expiry_date,
                                                                         option_type,
                                                                         option_price, calculation_date, volatility)
        delta_list.append(delta)
        gamma_list.append(gamma)
        theta_list.append(theta)
        vega_list.append(vega)
        rho_list.append(rho)

    return delta_list, gamma_list, theta_list, vega_list, rho_list


def payoff_charts(spot: list, strike: int, option_type: str, option_price: float, calculation_date: date,
                  expiry_date: date, volatility: float):
    spot = numpy.arange(min(spot), max(spot), 100, dtype=numpy.int64).tolist()

    if option_type in [Keys.call, Keys.put]:
        payoff_list = get_payoff_values(spot, strike, option_type, option_price)
        delta_list, gamma_list, theta_list, vega_list, rho_list = get_greeks_payoff_values(spot, strike, expiry_date,
                                                                                           calculation_date,
                                                                                           option_type,
                                                                                           option_price, volatility)

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

        py.plot(plotly_fig, filename="name.html")

    else:
        _logger.warning("Option can be either CE or PE")
        _logger.info("Couldn't plot payoffs")


if __name__ == '__main__':
    payoff_charts([9000, 11100], 10000, Keys.put, 276., date(2018, 10, 26), date(2018, 11, 29), 20.95)
