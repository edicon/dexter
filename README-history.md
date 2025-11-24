# Project History

## 2025-11-24: Crypto Tools Implementation

### Summary
Implemented cryptocurrency tools mirroring the existing finance tools structure to allow fetching crypto prices via the Financial Datasets API.

### Changes
1.  **New Module**: Created `src/dexter/tools/crypto/` directory.
    -   `api.py`: Dedicated API handler for crypto tools.
    -   `prices.py`: Implemented `get_crypto_price_snapshot` and `get_crypto_prices`.
    -   `__init__.py`: Exposed new tools.
2.  **Tool Registration**: Updated `src/dexter/tools/__init__.py` to register the new crypto tools.
3.  **Documentation**:
    -   Created `README-crypto.md` (English & Korean) explaining usage.
    -   Created `MAINTENANCE.md` guiding upstream sync and conflict resolution.

### Verification
-   Created and ran `src/dexter/tools/crypto/test_crypto.py` to verify API calls.
-   Simulated an upstream merge conflict to verify the maintenance guide.
