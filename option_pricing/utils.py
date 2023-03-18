# -*- coding: utf-8 -*-

from __future__ import annotations

from pydantic import BaseModel


class MarketData(BaseModel):
    """Market data dataclass needed for option pricing."""
    timestamp: str
    asset: str
    price: float
