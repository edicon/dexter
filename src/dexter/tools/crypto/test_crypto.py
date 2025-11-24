import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from dexter.tools.crypto.prices import get_crypto_price_snapshot, get_crypto_prices

def test_crypto_tools():
    print("Testing get_crypto_price_snapshot...")
    try:
        # Mocking the API call if no key is present or just testing the function call structure
        # For this test, we just want to ensure the function is callable and imports work.
        # If we have a key, it might actually work.
        snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
        print(f"Snapshot result: {snapshot}")
    except Exception as e:
        print(f"Snapshot test failed (expected if no API key): {e}")

    print("\nTesting get_crypto_prices...")
    try:
        prices = get_crypto_prices.invoke({
            "ticker": "BTC",
            "interval": "day",
            "interval_multiplier": 1,
            "start_date": "2023-01-01",
            "end_date": "2023-01-07"
        })
        print(f"Prices result: {prices}")
    except Exception as e:
        print(f"Prices test failed (expected if no API key): {e}")

if __name__ == "__main__":
    test_crypto_tools()
