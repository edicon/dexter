#!/usr/bin/env python3
"""Predict volatility for BTC, ETH, and XRP using Dexter agent."""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Load environment variables
load_dotenv()

from dexter.agent import Agent

def main():
    """Run Dexter agent to predict volatility for multiple cryptocurrencies."""
    agent = Agent()

    query = """
    Analyze Bitcoin (BTC), Ethereum (ETH), and Ripple (XRP) to predict volatility for the next 7 days.

    For EACH cryptocurrency, please perform the following analysis using the new tools:

    1. Technical Analysis:
       - Calculate technical indicators (ATR, RSI, MACD, Bollinger Bands) using `calculate_technical_indicators`
       - Interpret the indicators (e.g., is RSI overbought? is MACD bullish?)

    2. Volatility Analysis:
       - Calculate volatility metrics (Standard Deviation, Range-based, Parkinson, Garman-Klass) using `calculate_volatility_metrics`
       - Compare the different volatility metrics
       - Check if volatility is HIGH (>3%), MODERATE (1.5-3%), or LOW (<1.5%)

    3. News & Sentiment:
       - Search for recent news (last 7 days) for each asset
       - Assess market sentiment

    4. Prediction & Conclusion:
       - Provide a volatility forecast for the next 7 days (HIGH/MODERATE/LOW)
       - List key risk factors
       - Rate confidence (1-10)

    Please present the results in a structured format for each asset, followed by a comparative summary.
    """

    print("\n" + "="*80)
    print("Crypto Volatility Prediction - BTC, ETH, XRP")
    print("Analyzing technicals, volatility metrics, and news...")
    print("="*80 + "\n")

    answer = agent.run(query)

    print("\n" + "="*80)
    print("Analysis Complete")
    print("="*80)

if __name__ == "__main__":
    main()
