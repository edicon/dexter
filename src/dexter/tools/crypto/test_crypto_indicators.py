#!/usr/bin/env python3
"""Test technical indicators implementation."""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"))

from dexter.tools.crypto.indicators import calculate_technical_indicators


def test_technical_indicators():
    """Test all technical indicators for BTC."""
    print("\n" + "="*80)
    print("Testing Technical Indicators - Bitcoin (BTC)")
    print("="*80 + "\n")

    # Test with BTC
    result = calculate_technical_indicators.invoke({
        "ticker": "BTC",
        "indicators": ["atr", "rsi", "macd", "bollinger"],
        "period": 14,
        "data_count": 100
    })

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False

    print(f"📊 Ticker: {result['ticker']}")
    print(f"📈 Period: {result['period']}")
    print(f"📉 Data Points: {result['data_points']}")
    print()

    # Display ATR
    if "atr" in result["indicators"]:
        atr = result["indicators"]["atr"]
        print("🔥 ATR (Average True Range):")
        print(f"   Value: {atr['value']:,.0f} KRW")
        print(f"   Percent: {atr['percent']:.2f}%")
        print(f"   Interpretation: {atr['interpretation']}")
        print()

    # Display RSI
    if "rsi" in result["indicators"]:
        rsi = result["indicators"]["rsi"]
        print("📊 RSI (Relative Strength Index):")
        print(f"   Value: {rsi['value']:.2f}")
        print(f"   Interpretation: {rsi['interpretation']}")
        print()

    # Display MACD
    if "macd" in result["indicators"]:
        macd = result["indicators"]["macd"]
        print("📈 MACD:")
        print(f"   MACD Line: {macd['macd_line']:,.0f}")
        print(f"   Signal Line: {macd['signal_line']:,.0f}")
        print(f"   Histogram: {macd['histogram']:,.0f}")
        print(f"   Interpretation: {macd['interpretation']}")
        print()

    # Display Bollinger Bands
    if "bollinger" in result["indicators"]:
        bb = result["indicators"]["bollinger"]
        print("📉 Bollinger Bands:")
        print(f"   Upper: {bb['upper']:,.0f} KRW")
        print(f"   Middle: {bb['middle']:,.0f} KRW")
        print(f"   Lower: {bb['lower']:,.0f} KRW")
        print(f"   Bandwidth: {bb['bandwidth']:.2f}%")
        print(f"   %B: {bb['percent_b']:.2f}")
        print(f"   Interpretation: {bb['interpretation']}")
        print()

    print("="*80)
    print("✅ All technical indicators calculated successfully!")
    print("="*80)

    return True


if __name__ == "__main__":
    success = test_technical_indicators()
    sys.exit(0 if success else 1)
