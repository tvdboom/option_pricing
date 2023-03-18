# -*- coding: utf-8 -*-

import os
import sqlite3 as sl
from pathlib import Path

from option_pricing.utils import MarketData


# Get absolute path to parent directory
PARENT_DIR = str(Path(__file__).parent.parent.resolve())


class Market:
    """Manages the market table in market_db database.

    Class attributes
    ----------------
    con: sqlite connection
        Connection object to the market table.

    """

    con: sl.Connection = sl.connect(os.path.join(PARENT_DIR, "market_db"))

    @classmethod
    async def upload_data(cls, data: list[MarketData]):
        """Upload multiple rows of market data to the db.

        Parameters
        ----------
        data: list of MarketData
            Market data to upload.

        """
        query = """INSERT INTO market (timestamp, asset, price) VALUES (?, ?, ?)"""
        payload = list(map(lambda x: (x.timestamp, x.asset, x.price), data))

        try:
            cls.con.executemany(query, payload)
            cls.con.commit()
        except Exception as ex:
            raise ConnectionError(
                f"Failed to upload data {data} to the market table. Exception: {ex}"
            )

    @classmethod
    async def get_latest_prices(cls) -> dict[str, float]:
        """Retrieve the latest asset prices from the market.

        Returns
        -------
        dict
            Key is asset, value is price.

        """
        query = """
            SELECT asset, price
            FROM (
                SELECT
                    asset,
                    price,
                    row_number() over (partition by asset order by timestamp desc) rn
                FROM market
            )
            WHERE rn = 1
            """

        try:
            # Key=asset, value=price
            response = dict(cls.con.execute(query).fetchall())
        except Exception as ex:
            raise ConnectionError(
                f"Failed to get latest prices from the market table. Exception: {ex}"
            )

        return response
