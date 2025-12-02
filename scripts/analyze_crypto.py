#!/usr/bin/env python3
"""Analyze multiple cryptocurrencies using Dexter agent."""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Load environment variables
load_dotenv()

from dexter.agent import Agent

def main():
    """Run Dexter agent to analyze BTC, ETH, and XRP."""
    agent = Agent()

    # Analyze BTC, ETH, XRP
    query = """
    Analyze the performance of Bitcoin (BTC), Ethereum (ETH), and Ripple (XRP) over the past week.
    For each cryptocurrency, provide:
    1. Current price
    2. Weekly price change (percentage and absolute value)
    3. High and low prices in the past week
    4. Brief analysis of the trend

    Compare these three cryptocurrencies and provide insights.
    """

    print("\n" + "="*80)
    print("Analyzing BTC, ETH, and XRP...")
    print("="*80 + "\n")

    answer = agent.run(query)

    print("\n" + "="*80)
    print("Analysis Complete")
    print("="*80)

if __name__ == "__main__":
    main()
