# -*- coding: utf-8 -*-

import random
import string
from datetime import datetime, timedelta

import pytest

from option_pricing.market import Market
from option_pricing.utils import MarketData


def create_market_data(n: int, asset: bool = None) -> list[MarketData]:
    """Create dummy data for the market table.

    Parameters
    ----------
    n: int
        Number of rows to make.

    asset: bool, default=False
        Name of the asset to create. If None, create random ones.

    Returns
    -------
    list of MarketData
        Rows of timestamp, asset name and price.

    """
    data = []
    for _ in range(n):
        timestamp = str(datetime.now() - timedelta(minutes=random.randint(0, 1440)))
        name = asset or "".join(random.choices(string.ascii_lowercase, k=8))
        price = random.randint(1, 200)
        data.append(MarketData(timestamp=timestamp, asset=name, price=price))

    return data


@pytest.mark.asyncio
async def test_upload_data_to_market():
    """Assert that the data is correctly uploaded to the market table."""
    query = """SELECT count(*) FROM market ORDER BY timestamp DESC"""

    # Count number of current rows in market table
    old_length = Market.con.execute(query).fetchone()[0]

    # Add 10 random rows
    await Market.upload_data(create_market_data(10))

    # Check number of rows increased
    assert Market.con.execute(query).fetchone()[0] == old_length + 10


@pytest.mark.asyncio
async def test_get_latest_prices():
    """Assert that the latest asset prices can be retrieved."""
    # Create a random asset and add 10 rows to market table
    asset = "".join(random.choices(string.ascii_lowercase, k=8))
    data = create_market_data(10, asset=asset)
    await Market.upload_data(data)

    response = await Market.get_latest_prices()

    # Check that all assets are returned
    query = """SELECT count(*) FROM market GROUP BY asset"""
    assert len(response) == len(Market.con.execute(query).fetchall())

    # Check that the returned value is the latest price
    assert response[asset] == max(data, key=lambda x: x.timestamp).price
