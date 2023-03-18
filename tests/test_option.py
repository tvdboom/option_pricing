# -*- coding: utf-8 -*-

from datetime import date

import numpy as np

from option_pricing.option import Option, OptionsHandler


def test_option_parsing():
    """Assert that the option object parses the input correctly."""
    option = Option("BRN Jan24 Call Strike 100 USD/BBL")
    assert option.asset == "BRN"
    assert option.delivery_date == "Jan24"
    assert option.is_call == 1
    assert option.strike_price == 100
    assert option.unit == "USD/BBL"


def test_option_maturity():
    """Assert that the maturity date is calculated correctly."""
    days_diff = date(year=2023, month=11, day=30) - date.today()

    option = Option("BRN Jan24 Call Strike 100 USD/BBL")
    assert option.get_maturity_in_years() == days_diff.days / 365.25


def test_black76():
    """Assert that the black76 formula works correctly."""
    handler = OptionsHandler([])
    black = handler.black76(
        np.array([42]), np.array([42]), np.array([1.5]), 0.05, 0.2, np.array([0])
    )
    assert np.around(black, 3) == np.array([3.798])  # Calculated manually
