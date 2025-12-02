"""
Technical indicators calculation for cryptocurrency analysis.

This module provides functions to calculate various technical indicators
used in volatility analysis and trading decisions.
"""

from langchain.tools import tool
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from dexter.tools.crypto.api import call_api


def _get_price_data(ticker: str, count: int = 100) -> pd.DataFrame:
    """
    Fetch historical price data and convert to DataFrame.

    Args:
        ticker: Cryptocurrency ticker symbol
        count: Number of candles to retrieve

    Returns:
        DataFrame with OHLC data
    """
    # Handle ticker format
    market = ticker.upper()
    if "-" not in market:
        market = f"KRW-{market}"

    # Fetch data from Upbit API
    endpoint = "/candles/days"
    params = {"market": market, "count": count}

    try:
        data = call_api(endpoint, params)
        if not data:
            return pd.DataFrame()

        # Convert to DataFrame and reverse (oldest first)
        df = pd.DataFrame(data)
        df = df.iloc[::-1].reset_index(drop=True)

        # Rename columns to standard OHLC format
        df = df.rename(columns={
            'opening_price': 'open',
            'high_price': 'high',
            'low_price': 'low',
            'trade_price': 'close',
            'candle_date_time_kst': 'timestamp'
        })

        return df[['timestamp', 'open', 'high', 'low', 'close']]

    except Exception as e:
        raise Exception(f"Failed to fetch price data: {str(e)}")


def calculate_atr(df: pd.DataFrame, period: int = 14) -> dict:
    """
    Calculate Average True Range (ATR) - volatility indicator.

    ATR measures market volatility by decomposing the entire range of an asset
    price for that period.
    """
    if len(df) < period + 1:
        return {"error": f"Insufficient data. Need at least {period + 1} candles."}

    # Calculate True Range
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift(1))
    low_close = abs(df['low'] - df['close'].shift(1))

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

    # Calculate ATR as moving average of True Range
    atr = true_range.rolling(window=period).mean()
    current_atr = atr.iloc[-1]

    # Calculate ATR as percentage of price
    current_price = df['close'].iloc[-1]
    atr_percent = (current_atr / current_price) * 100

    # Interpretation
    if atr_percent >= 3.0:
        interpretation = "HIGH volatility"
    elif atr_percent >= 1.5:
        interpretation = "MODERATE volatility"
    else:
        interpretation = "LOW volatility"

    return {
        "value": float(current_atr),
        "percent": float(atr_percent),
        "interpretation": interpretation
    }


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> dict:
    """
    Calculate Relative Strength Index (RSI) - momentum indicator.

    RSI measures the magnitude of recent price changes to evaluate
    overbought or oversold conditions (0-100 scale).
    """
    if len(df) < period + 1:
        return {"error": f"Insufficient data. Need at least {period + 1} candles."}

    # Calculate price changes
    delta = df['close'].diff()

    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()

    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    current_rsi = rsi.iloc[-1]

    # Interpretation
    if current_rsi >= 70:
        interpretation = "Overbought - potential reversal down"
    elif current_rsi <= 30:
        interpretation = "Oversold - potential reversal up"
    elif current_rsi >= 60:
        interpretation = "Approaching overbought"
    elif current_rsi <= 40:
        interpretation = "Approaching oversold"
    else:
        interpretation = "Neutral"

    return {
        "value": float(current_rsi),
        "interpretation": interpretation
    }


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """
    Calculate MACD (Moving Average Convergence Divergence).

    MACD is a trend-following momentum indicator showing the relationship
    between two moving averages of a security's price.
    """
    if len(df) < slow + signal:
        return {"error": f"Insufficient data. Need at least {slow + signal} candles."}

    # Calculate EMAs
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

    # Calculate MACD line
    macd_line = ema_fast - ema_slow

    # Calculate signal line
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()

    # Calculate histogram
    histogram = macd_line - signal_line

    current_macd = macd_line.iloc[-1]
    current_signal = signal_line.iloc[-1]
    current_histogram = histogram.iloc[-1]
    previous_histogram = histogram.iloc[-2]

    # Interpretation
    if current_histogram > 0 and previous_histogram <= 0:
        interpretation = "Bullish crossover - buy signal"
    elif current_histogram < 0 and previous_histogram >= 0:
        interpretation = "Bearish crossover - sell signal"
    elif current_histogram > 0:
        interpretation = "Bullish momentum"
    else:
        interpretation = "Bearish momentum"

    return {
        "macd_line": float(current_macd),
        "signal_line": float(current_signal),
        "histogram": float(current_histogram),
        "interpretation": interpretation
    }


def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, num_std: float = 2.0) -> dict:
    """
    Calculate Bollinger Bands - volatility indicator.

    Bollinger Bands consist of a middle band (SMA) and two outer bands
    (standard deviations away from the middle band).
    """
    if len(df) < period:
        return {"error": f"Insufficient data. Need at least {period} candles."}

    # Calculate middle band (SMA)
    middle_band = df['close'].rolling(window=period).mean()

    # Calculate standard deviation
    std = df['close'].rolling(window=period).std()

    # Calculate upper and lower bands
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)

    current_price = df['close'].iloc[-1]
    current_upper = upper_band.iloc[-1]
    current_middle = middle_band.iloc[-1]
    current_lower = lower_band.iloc[-1]

    # Calculate bandwidth (volatility measure)
    bandwidth = ((current_upper - current_lower) / current_middle) * 100

    # Calculate %B (position within bands)
    percent_b = (current_price - current_lower) / (current_upper - current_lower)

    # Interpretation
    if bandwidth >= 10:
        volatility_state = "HIGH volatility"
    elif bandwidth >= 5:
        volatility_state = "MODERATE volatility"
    else:
        volatility_state = "LOW volatility"

    if percent_b >= 1.0:
        price_position = "Above upper band - overbought"
    elif percent_b <= 0.0:
        price_position = "Below lower band - oversold"
    elif percent_b >= 0.8:
        price_position = "Near upper band"
    elif percent_b <= 0.2:
        price_position = "Near lower band"
    else:
        price_position = "Within normal range"

    return {
        "upper": float(current_upper),
        "middle": float(current_middle),
        "lower": float(current_lower),
        "bandwidth": float(bandwidth),
        "percent_b": float(percent_b),
        "volatility": volatility_state,
        "price_position": price_position,
        "interpretation": f"{volatility_state}. Price is {price_position.lower()}."
    }


class TechnicalIndicatorsInput(BaseModel):
    """Input schema for calculate_technical_indicators."""
    ticker: str = Field(..., description="Cryptocurrency ticker symbol (e.g., 'BTC', 'ETH', 'KRW-BTC')")
    indicators: List[Literal["atr", "rsi", "macd", "bollinger"]] = Field(
        default=["atr", "rsi", "macd", "bollinger"],
        description="List of indicators to calculate"
    )
    period: int = Field(default=14, description="Period for indicator calculations (default: 14)")
    data_count: int = Field(default=100, description="Number of candles to fetch for calculations (default: 100)")


@tool(args_schema=TechnicalIndicatorsInput)
def calculate_technical_indicators(
    ticker: str,
    indicators: List[Literal["atr", "rsi", "macd", "bollinger"]] = ["atr", "rsi", "macd", "bollinger"],
    period: int = 14,
    data_count: int = 100
) -> dict:
    """
    Calculate technical indicators for cryptocurrency analysis.

    Provides various technical indicators used in volatility and trend analysis:
    - ATR (Average True Range): Measures market volatility
    - RSI (Relative Strength Index): Identifies overbought/oversold conditions
    - MACD: Shows trend direction and momentum
    - Bollinger Bands: Indicates volatility and price levels

    Args:
        ticker: Cryptocurrency ticker symbol
        indicators: List of indicators to calculate
        period: Period for calculations (default: 14)
        data_count: Number of candles to fetch (default: 100)

    Returns:
        Dictionary containing calculated indicators and interpretations
    """
    try:
        # Fetch price data
        df = _get_price_data(ticker, data_count)

        if df.empty:
            return {"error": "Failed to fetch price data"}

        # Calculate requested indicators
        results = {
            "ticker": ticker,
            "period": period,
            "data_points": len(df),
            "indicators": {}
        }

        if "atr" in indicators:
            results["indicators"]["atr"] = calculate_atr(df, period)

        if "rsi" in indicators:
            results["indicators"]["rsi"] = calculate_rsi(df, period)

        if "macd" in indicators:
            results["indicators"]["macd"] = calculate_macd(df)

        if "bollinger" in indicators:
            results["indicators"]["bollinger"] = calculate_bollinger_bands(df, period)

        return results

    except Exception as e:
        return {"error": f"Failed to calculate indicators: {str(e)}"}
