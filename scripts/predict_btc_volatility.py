#!/usr/bin/env python3
"""Predict BTC volatility using historical data and news analysis."""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Load environment variables
load_dotenv()

from dexter.agent import Agent

def main():
    """Run Dexter agent to predict BTC volatility."""
    agent = Agent()

    query = """
    Analyze Bitcoin (BTC) to predict volatility for the next 7 days.

    Please perform the following analysis:

    1. Historical Price Analysis:
       - Fetch the last 30 days of daily price data
       - Fetch the last 200 days of daily price data
       - Calculate daily volatility (high-low range) for each period
       - Identify patterns, trends, and volatility clusters
       - Compare recent 30-day volatility vs 200-day average

    2. Recent News Analysis:
       - Search for recent Bitcoin news (last 7 days)
       - Identify key events, regulatory changes, or market sentiment
       - Assess how news might impact short-term volatility

    3. Volatility Prediction (Next 7 Days):
       - Based on historical patterns from 200-day data
       - Based on recent 30-day trends
       - Based on news sentiment and upcoming events
       - Provide a volatility forecast: HIGH (>5%), MODERATE (2-5%), or LOW (<2%)
       - List key risk factors that could increase volatility
       - List stabilizing factors that could reduce volatility

    4. Confidence Level:
       - Rate your prediction confidence (1-10)
       - Explain the reasoning

    Please follow the Financial Analysis Rules in GEMINI.md:
    - Show raw data for recent days
    - Calculate daily ranges explicitly
    - Weight recent 3-day data heavily
    - Don't underestimate volatility
    """

    print("\n" + "="*80)
    print("BTC Volatility Prediction - Next 7 Days")
    print("Analyzing 200-day history, 30-day trends, and recent news...")
    print("="*80 + "\n")

    answer = agent.run(query)

    print("\n" + "="*80)
    print("Analysis Complete")
    print("="*80)

if __name__ == "__main__":
    main()
