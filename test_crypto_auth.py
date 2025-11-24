import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

# Load environment variables
load_dotenv()

from dexter.tools.crypto.prices import get_crypto_price_snapshot

def main():
    print("Testing get_crypto_price_snapshot with credentials...")
    try:
        snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
        print(f"Snapshot result: {snapshot}")
    except Exception as e:
        print(f"Snapshot test failed: {e}")

if __name__ == "__main__":
    main()
