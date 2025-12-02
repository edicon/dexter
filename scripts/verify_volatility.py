#!/usr/bin/env python3
"""Verify actual volatility of BTC, ETH, XRP over the past 3 days."""
import os
import sys
import requests
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Load environment variables
load_dotenv()

def get_upbit_prices(ticker: str, days: int = 3):
    """Get price data directly from Upbit API."""
    url = f"https://api.upbit.com/v1/candles/days"
    params = {
        "market": ticker,
        "count": days
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def analyze_volatility(ticker: str, days: int = 3):
    """Analyze volatility for a given ticker over specified days."""
    print(f"\n{'='*80}")
    print(f"Analyzing {ticker} - Past {days} Days")
    print(f"{'='*80}")

    try:
        prices = get_upbit_prices(ticker, days)
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return

    if not prices:
        print(f"❌ Empty price data for {ticker}")
        return

    # Calculate statistics
    highs = [p['high_price'] for p in prices]
    lows = [p['low_price'] for p in prices]
    opens = [p['opening_price'] for p in prices]
    closes = [p['trade_price'] for p in prices]

    max_high = max(highs)
    min_low = min(lows)
    first_open = opens[0]
    last_close = closes[-1]

    # Calculate volatility metrics
    range_volatility = ((max_high - min_low) / min_low) * 100
    price_change = ((last_close - first_open) / first_open) * 100

    print(f"\n📊 Raw Data:")
    for i, p in enumerate(prices):
        date = p.get('candle_date_time_kst', p.get('candle_date_time_utc', 'N/A'))
        print(f"  Day {i+1} ({date[:10]}):")
        print(f"    Open: {p['opening_price']:,.0f} KRW")
        print(f"    High: {p['high_price']:,.0f} KRW")
        print(f"    Low:  {p['low_price']:,.0f} KRW")
        print(f"    Close: {p['trade_price']:,.0f} KRW")
        daily_range = ((p['high_price'] - p['low_price']) / p['low_price']) * 100
        print(f"    Daily Range: {daily_range:.2f}%")

    print(f"\n📈 Summary Statistics:")
    print(f"  Highest Price: {max_high:,.0f} KRW")
    print(f"  Lowest Price: {min_low:,.0f} KRW")
    print(f"  First Open: {first_open:,.0f} KRW")
    print(f"  Last Close: {last_close:,.0f} KRW")
    print(f"\n🔥 Volatility Metrics:")
    print(f"  Range Volatility (High-Low): {range_volatility:.2f}%")
    print(f"  Price Change (Open-Close): {price_change:+.2f}%")

    # Volatility assessment
    if range_volatility >= 3.0:
        assessment = "⚠️  HIGH VOLATILITY"
    elif range_volatility >= 1.5:
        assessment = "📊 MODERATE VOLATILITY"
    else:
        assessment = "✅ LOW VOLATILITY"

    print(f"\n{assessment}")
    print(f"{'='*80}\n")

def main():
    """Verify volatility for BTC, ETH, and XRP."""
    print("\n" + "="*80)
    print("VOLATILITY VERIFICATION - Past 3 Days")
    print("="*80)

    analyze_volatility("KRW-BTC", days=3)
    analyze_volatility("KRW-ETH", days=3)
    analyze_volatility("KRW-XRP", days=3)

    print("\n" + "="*80)
    print("Verification Complete")
    print("="*80)

if __name__ == "__main__":
    main()
