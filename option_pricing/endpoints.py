# -*- coding: utf-8 -*-

from fastapi import FastAPI

from option_pricing.market import Market
from option_pricing.option import OptionsHandler
from option_pricing.utils import MarketData

app = FastAPI()


@app.post("/market/upload_data/")
async def upload_market_data(payload: list[MarketData]):
    """Upload multiple rows of market data to the db."""
    await Market.upload_data(payload)


@app.get("/market/get_latest_prices/")
async def get_latest_prices() -> dict[str, float]:
    """Retrieve the latest asset prices from the market."""
    return await Market.get_latest_prices()


@app.post("/options/calculate_pv/")
async def calculate_pv(payload: list[str]) -> list[float]:
    handler = OptionsHandler(payload)
    future_prices = await get_latest_prices()

    return handler.calculate_pv(future_prices)
