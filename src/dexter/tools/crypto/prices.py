from langchain.tools import tool
from typing import Literal, Optional
from pydantic import BaseModel, Field
from dexter.tools.crypto.api import call_api
from datetime import datetime

class CryptoPriceSnapshotInput(BaseModel):
    """Input for get_crypto_price_snapshot."""
    ticker: str = Field(..., description="The crypto ticker symbol. For example, 'BTC' or 'KRW-BTC'. Defaults to KRW market if no prefix provided.")

@tool(args_schema=CryptoPriceSnapshotInput)
def get_crypto_price_snapshot(ticker: str) -> dict:
    """
    Fetches the most recent price snapshot for a specific cryptocurrency from Upbit.
    """
    # Handle ticker format: default to KRW- if no hyphen found
    market = ticker.upper()
    if "-" not in market:
        market = f"KRW-{market}"

    params = {"markets": market}
    try:
        data = call_api("/ticker", params)
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            # Map Upbit response to a generic snapshot format
            return {
                "ticker": item.get("market"),
                "price": item.get("trade_price"),
                "open": item.get("opening_price"),
                "high": item.get("high_price"),
                "low": item.get("low_price"),
                "volume": item.get("acc_trade_volume_24h"),
                "timestamp": item.get("timestamp"),
                "date": item.get("trade_date_kst"),
                "time": item.get("trade_time_kst"),
            }
        return {"error": "No data found"}
    except Exception as e:
        return {"error": str(e)}

class CryptoPricesInput(BaseModel):
    """Input for get_crypto_prices."""
    ticker: str = Field(..., description="The crypto ticker symbol. For example, 'BTC' or 'KRW-BTC'.")
    interval: Literal["minute", "day", "week", "month"] = Field(default="day", description="The time interval. 'year' is not supported by Upbit.")
    interval_multiplier: int = Field(default=1, description="Multiplier for the interval (only for minutes: 1, 3, 5, 10, 15, 30, 60, 240).")
    count: int = Field(default=20, description="Number of candles to retrieve.")
    to: Optional[str] = Field(None, description="Last candle time (ISO8601 or 'yyyy-MM-dd HH:mm:ss'). Defaults to now.")

@tool(args_schema=CryptoPricesInput)
def get_crypto_prices(
    ticker: str,
    interval: Literal["minute", "day", "week", "month"],
    interval_multiplier: int = 1,
    count: int = 20,
    to: Optional[str] = None,
) -> list:
    """
    Retrieves historical price candles for a cryptocurrency from Upbit.
    """
    # Handle ticker format
    market = ticker.upper()
    if "-" not in market:
        market = f"KRW-{market}"

    # Construct endpoint based on interval
    if interval == "minute":
        # Upbit supports specific minute units
        valid_minutes = [1, 3, 5, 10, 15, 30, 60, 240]
        unit = interval_multiplier if interval_multiplier in valid_minutes else 1
        endpoint = f"/candles/minutes/{unit}"
    elif interval == "day":
        endpoint = "/candles/days"
    elif interval == "week":
        endpoint = "/candles/weeks"
    elif interval == "month":
        endpoint = "/candles/months"
    else:
        return [{"error": f"Unsupported interval: {interval}"}]

    params = {
        "market": market,
        "count": count,
    }
    if to:
        params["to"] = to

    try:
        data = call_api(endpoint, params)
        # Upbit returns a list of candles directly
        return data
    except Exception as e:
        return [{"error": str(e)}]
