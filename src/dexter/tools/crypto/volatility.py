"""
Volatility metrics calculation for cryptocurrency analysis.

This module provides various methods to calculate and measure volatility,
each offering different perspectives on market risk and price movements.
"""

from langchain.tools import tool
from typing import List, Literal
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


def _classify_volatility(volatility: float) -> str:
    """Classify volatility level based on GEMINI.md rules."""
    if volatility >= 3.0:
        return "HIGH"
    elif volatility >= 1.5:
        return "MODERATE"
    else:
        return "LOW"


def calculate_std_volatility(df: pd.DataFrame, period: int = 30) -> dict:
    """
    Calculate Standard Deviation-based volatility.

    This is the most common volatility measure, using the standard deviation
    of returns over a specified period.

    Args:
        df: DataFrame with OHLC data
        period: Number of periods for calculation

    Returns:
        Dict with daily and annualized volatility
    """
    if len(df) < period + 1:
        return {"error": f"Insufficient data. Need at least {period + 1} candles."}

    # Calculate returns
    returns = df['close'].pct_change().dropna()

    # Calculate daily volatility (standard deviation of returns)
    daily_vol = returns.tail(period).std()

    # Annualized volatility (assuming 365 trading days for crypto)
    annualized_vol = daily_vol * np.sqrt(365)

    # Convert to percentage
    daily_vol_pct = daily_vol * 100
    annualized_vol_pct = annualized_vol * 100

    return {
        "daily": float(daily_vol_pct),
        "annualized": float(annualized_vol_pct),
        "classification": _classify_volatility(daily_vol_pct)
    }


def calculate_range_volatility(df: pd.DataFrame, period: int = 30) -> dict:
    """
    Calculate Range-based volatility.

    This method uses the high-low range as defined in GEMINI.md:
    ((period_high - period_low) / period_low) * 100

    Args:
        df: DataFrame with OHLC data
        period: Number of periods for calculation

    Returns:
        Dict with range volatility and classification
    """
    if len(df) < period:
        return {"error": f"Insufficient data. Need at least {period} candles."}

    # Get data for the period
    period_data = df.tail(period)

    # Calculate range volatility
    period_high = period_data['high'].max()
    period_low = period_data['low'].min()

    range_vol = ((period_high - period_low) / period_low) * 100

    # Also calculate daily ranges for context
    daily_ranges = []
    for _, row in period_data.iterrows():
        daily_range = ((row['high'] - row['low']) / row['low']) * 100
        daily_ranges.append(daily_range)

    max_daily_range = max(daily_ranges)
    avg_daily_range = sum(daily_ranges) / len(daily_ranges)

    return {
        "value": float(range_vol),
        "max_daily_range": float(max_daily_range),
        "avg_daily_range": float(avg_daily_range),
        "classification": _classify_volatility(range_vol)
    }


def calculate_parkinson_volatility(df: pd.DataFrame, period: int = 30) -> dict:
    """
    Calculate Parkinson's Volatility.

    Parkinson's volatility uses only high and low prices, making it more
    efficient than close-to-close volatility estimators.

    Formula: sqrt(1/(4*N*ln(2)) * sum(ln(Hi/Li)^2))

    Args:
        df: DataFrame with OHLC data
        period: Number of periods for calculation

    Returns:
        Dict with Parkinson volatility
    """
    if len(df) < period:
        return {"error": f"Insufficient data. Need at least {period} candles."}

    # Get data for the period
    period_data = df.tail(period)

    # Calculate Parkinson's volatility
    hl_ratio = np.log(period_data['high'] / period_data['low'])
    parkinson_var = (1 / (4 * period * np.log(2))) * (hl_ratio ** 2).sum()
    parkinson_vol = np.sqrt(parkinson_var)

    # Annualize (assuming 365 trading days)
    annualized_parkinson = parkinson_vol * np.sqrt(365)

    # Convert to percentage
    parkinson_vol_pct = parkinson_vol * 100
    annualized_pct = annualized_parkinson * 100

    return {
        "value": float(parkinson_vol_pct),
        "annualized": float(annualized_pct),
        "classification": _classify_volatility(parkinson_vol_pct)
    }


def calculate_garman_klass_volatility(df: pd.DataFrame, period: int = 30) -> dict:
    """
    Calculate Garman-Klass Volatility.

    Garman-Klass estimator uses open, high, low, and close prices,
    providing a more accurate volatility estimate than simpler methods.

    Formula: sqrt(1/N * sum(0.5*(ln(Hi/Li))^2 - (2ln(2)-1)*(ln(Ci/Oi))^2))

    Args:
        df: DataFrame with OHLC data
        period: Number of periods for calculation

    Returns:
        Dict with Garman-Klass volatility
    """
    if len(df) < period:
        return {"error": f"Insufficient data. Need at least {period} candles."}

    # Get data for the period
    period_data = df.tail(period)

    # Calculate components
    hl_component = 0.5 * (np.log(period_data['high'] / period_data['low']) ** 2)
    co_component = (2 * np.log(2) - 1) * (np.log(period_data['close'] / period_data['open']) ** 2)

    # Calculate Garman-Klass variance
    gk_var = (1 / period) * (hl_component - co_component).sum()
    gk_vol = np.sqrt(gk_var)

    # Annualize
    annualized_gk = gk_vol * np.sqrt(365)

    # Convert to percentage
    gk_vol_pct = gk_vol * 100
    annualized_pct = annualized_gk * 100

    return {
        "value": float(gk_vol_pct),
        "annualized": float(annualized_pct),
        "classification": _classify_volatility(gk_vol_pct)
    }


class VolatilityMetricsInput(BaseModel):
    """Input schema for calculate_volatility_metrics."""
    ticker: str = Field(..., description="Cryptocurrency ticker symbol (e.g., 'BTC', 'ETH', 'KRW-BTC')")
    period: int = Field(default=30, description="Period for volatility calculation in days (default: 30)")
    methods: List[Literal["std", "range", "parkinson", "garman_klass"]] = Field(
        default=["std", "range", "parkinson", "garman_klass"],
        description="List of volatility calculation methods to use"
    )


@tool(args_schema=VolatilityMetricsInput)
def calculate_volatility_metrics(
    ticker: str,
    period: int = 30,
    methods: List[Literal["std", "range", "parkinson", "garman_klass"]] = ["std", "range", "parkinson", "garman_klass"]
) -> dict:
    """
    Calculate cryptocurrency volatility using multiple methods.

    Provides comprehensive volatility analysis using different calculation methods:
    - Standard Deviation: Classic volatility measure based on returns
    - Range-based: Uses high-low range (GEMINI.md method)
    - Parkinson's: Efficient estimator using only high/low prices
    - Garman-Klass: Advanced estimator using all OHLC prices

    Each method provides a different perspective on market volatility and risk.

    Args:
        ticker: Cryptocurrency ticker symbol
        period: Number of days for calculation (default: 30)
        methods: List of calculation methods to use

    Returns:
        Dictionary containing volatility metrics and consensus analysis
    """
    try:
        # Fetch price data (need extra data for some calculations)
        df = _get_price_data(ticker, count=period + 50)

        if df.empty:
            return {"error": "Failed to fetch price data"}

        # Calculate requested metrics
        results = {
            "ticker": ticker,
            "period": period,
            "data_points": len(df),
            "volatility_metrics": {}
        }

        if "std" in methods:
            results["volatility_metrics"]["standard_deviation"] = calculate_std_volatility(df, period)

        if "range" in methods:
            results["volatility_metrics"]["range_based"] = calculate_range_volatility(df, period)

        if "parkinson" in methods:
            results["volatility_metrics"]["parkinson"] = calculate_parkinson_volatility(df, period)

        if "garman_klass" in methods:
            results["volatility_metrics"]["garman_klass"] = calculate_garman_klass_volatility(df, period)

        # Generate consensus analysis
        classifications = []
        for method_name, method_data in results["volatility_metrics"].items():
            if "classification" in method_data:
                classifications.append(method_data["classification"])

        if classifications:
            # Count classifications
            high_count = classifications.count("HIGH")
            moderate_count = classifications.count("MODERATE")
            low_count = classifications.count("LOW")
            total = len(classifications)

            # Determine consensus
            if high_count >= total * 0.5:
                consensus = "All methods indicate HIGH volatility"
            elif moderate_count >= total * 0.5:
                consensus = "Methods indicate MODERATE volatility"
            elif low_count >= total * 0.5:
                consensus = "Methods indicate LOW volatility"
            elif high_count > 0:
                consensus = f"Mixed signals with {high_count}/{total} methods showing HIGH volatility"
            else:
                consensus = "Mixed volatility signals across methods"

            results["comparison"] = consensus
            results["classification_breakdown"] = {
                "HIGH": high_count,
                "MODERATE": moderate_count,
                "LOW": low_count
            }

        return results

    except Exception as e:
        return {"error": f"Failed to calculate volatility metrics: {str(e)}"}
