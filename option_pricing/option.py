# -*- coding: utf-8 -*-

import re
from calendar import monthcalendar
from datetime import date, datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from numba import jit
from scipy.stats import norm


class Option:
    """Properties for a single option."""

    pattern = "([A-Z]+?) ([a-zA-Z]{3}\d{2}) (Call|Put) Strike (\d+?) (.+)"
    delivery_to_maturity = dict(BRN=2, HH=1)

    def __init__(self, data: str):
        # Parse option
        regex = re.match(self.pattern, data)

        if not regex or len(regex.groups()) != 5:
            raise ValueError(f"Unable to parse option {data}.")

        # TODO: Add checks that the parsing was correct
        self.asset = regex.groups()[0]
        self.delivery_date = regex.groups()[1]
        self.is_call = int(regex.groups()[2] == "Call")
        self.strike_price = float(regex.groups()[3])
        self.unit = regex.groups()[4]

    def get_maturity_in_years(self) -> float:
        """Calculate the maturity period.

        Returns
        -------
        float
            Maturity in years.

        """
        # Extract maturity month and year from delivery date
        t = datetime.strptime(f"{self.delivery_date}{date.today().year}", "%b%d%Y")
        t = t - relativedelta(months=self.delivery_to_maturity.get(self.asset, 1))

        # Assumption: All options have a maturity_date > today
        if t < datetime.now():
            t = date(t.year + 1, t.month, max(monthcalendar(t.year + 1, t.month)[-1][:5]))
        else:
            t = date(t.year, t.month, max(monthcalendar(t.year, t.month)[-1][:5]))

        return (t - date.today()).days / 365.25


class OptionsHandler:
    """Collects a group of options to operate on."""

    risk_free_rate: float = 0.05
    volatility: float = 0.20

    def __init__(self, data: list[str]):
        options = []
        for elem in data:
            o = Option(elem)
            options.append(
                (o.asset, o.get_maturity_in_years(), o.is_call, o.strike_price, o.unit)
            )

        # Create table with overview of options in handler
        self.options = pd.DataFrame(
            data=options,
            columns=["asset", "maturity", "is_call", "strike_price", "unit"],
        )

    @staticmethod
    @jit(forceobj=True)
    def black76(
        F: np.ndarray,
        K: np.ndarray,
        T: np.ndarray,
        r: float,
        sigma: float,
        is_call: np.ndarray,
    ) -> np.ndarray:
        """Option pricing calculator using Black76 formula.

        Parameters
        ----------
        F: np.ndarray
            Future price.

        K: np.ndarray
            Strike price.

        T: np.ndarray
            Maturity period in years.

        r: float
            Risk-free rate.

        sigma: float
            Volatility.

        is_call: np.ndarray
            1 if Call, 0 if Put.

        Returns
        -------
        np.ndarray
            PV per provided option.

        Notes
        -----
        See https://en.wikipedia.org/wiki/Black_model.

        """
        # TODO: investigate how to compile native scipy.stats.norm to use with njit
        cdf = lambda x: norm.cdf(x, 0, 1)

        d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        return np.where(
            is_call == 1,
            np.exp(-r * T) * (F * cdf(d1) - K * cdf(d2)),
            np.exp(-r * T) * (K * cdf(-d2) - F * cdf(-d1)),
        )

    def calculate_pv(self, future_prices: dict[str, float]) -> list[float]:
        """Calculate the options' PV using Black76.

        Parameters
        ----------
        future_prices: dict
            Future prices as returned by Market.get_latest_prices.

        Returns
        -------
        list of float
            Calculated PV of options using Black76.

        """
        # Vectorize parameters for calculation
        F = np.array(list(map(lambda x: future_prices[x], self.options["asset"])))
        K = self.options["strike_price"].values
        T = self.options["maturity"].values  # maturity
        r = self.risk_free_rate
        sigma = self.volatility
        is_call = self.options["is_call"].values

        return list(self.black76(F, K, T, r, sigma, is_call))
