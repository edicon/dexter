import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Load environment variables
load_dotenv()

from dexter.tools.crypto.prices import get_crypto_price_snapshot, get_crypto_prices

def main():
    print("Testing get_crypto_price_snapshot (Upbit)...")
    try:
        snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
        print(f"Snapshot result: {snapshot}")
    except Exception as e:
        print(f"Snapshot test failed: {e}")

    print("\nTesting get_crypto_prices (Upbit)...")
    try:
        prices = get_crypto_prices.invoke({
            "ticker": "BTC",
            "interval": "day",
            "count": 5
        })
        print(f"Prices result (first 2): {prices[:2]}")
    except Exception as e:
        print(f"Prices test failed: {e}")

if __name__ == "__main__":
    main()
