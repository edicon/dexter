#!/usr/bin/env python3
"""Test volatility metrics implementation."""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"))

from dexter.tools.crypto.volatility import calculate_volatility_metrics


def test_volatility_metrics():
    """Test all volatility calculation methods for BTC."""
    print("\n" + "="*80)
    print("Testing Volatility Metrics - Bitcoin (BTC)")
    print("="*80 + "\n")

    # Test with BTC over 30 days
    result = calculate_volatility_metrics.invoke({
        "ticker": "BTC",
        "period": 30,
        "methods": ["std", "range", "parkinson", "garman_klass"]
    })

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False

    print(f"📊 Ticker: {result['ticker']}")
    print(f"📈 Period: {result['period']} days")
    print(f"📉 Data Points: {result['data_points']}")
    print()

    # Display Standard Deviation
    if "standard_deviation" in result["volatility_metrics"]:
        std = result["volatility_metrics"]["standard_deviation"]
        print("📊 Standard Deviation Volatility:")
        print(f"   Daily: {std['daily']:.2f}%")
        print(f"   Annualized: {std['annualized']:.2f}%")
        print(f"   Classification: {std['classification']}")
        print()

    # Display Range-based
    if "range_based" in result["volatility_metrics"]:
        rng = result["volatility_metrics"]["range_based"]
        print("📈 Range-based Volatility (GEMINI.md method):")
        print(f"   Period Range: {rng['value']:.2f}%")
        print(f"   Max Daily Range: {rng['max_daily_range']:.2f}%")
        print(f"   Avg Daily Range: {rng['avg_daily_range']:.2f}%")
        print(f"   Classification: {rng['classification']}")
        print()

    # Display Parkinson's
    if "parkinson" in result["volatility_metrics"]:
        park = result["volatility_metrics"]["parkinson"]
        print("🔬 Parkinson's Volatility:")
        print(f"   Value: {park['value']:.2f}%")
        print(f"   Annualized: {park['annualized']:.2f}%")
        print(f"   Classification: {park['classification']}")
        print()

    # Display Garman-Klass
    if "garman_klass" in result["volatility_metrics"]:
        gk = result["volatility_metrics"]["garman_klass"]
        print("🔬 Garman-Klass Volatility:")
        print(f"   Value: {gk['value']:.2f}%")
        print(f"   Annualized: {gk['annualized']:.2f}%")
        print(f"   Classification: {gk['classification']}")
        print()

    # Display consensus
    if "comparison" in result:
        print("🎯 Consensus Analysis:")
        print(f"   {result['comparison']}")
        print()

        if "classification_breakdown" in result:
            breakdown = result["classification_breakdown"]
            print("   Classification Breakdown:")
            print(f"   - HIGH: {breakdown['HIGH']} methods")
            print(f"   - MODERATE: {breakdown['MODERATE']} methods")
            print(f"   - LOW: {breakdown['LOW']} methods")
            print()

    print("="*80)
    print("✅ All volatility metrics calculated successfully!")
    print("="*80)

    return True


if __name__ == "__main__":
    success = test_volatility_metrics()
    sys.exit(0 if success else 1)
