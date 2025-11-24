# Project History

## 2025-11-24: Crypto Tools Implementation

### Summary
Implemented cryptocurrency tools mirroring the existing finance tools structure. Initially used Financial Datasets API, but migrated to **Upbit API** to provide free access to crypto data without API keys.

### Changes
1.  **New Module**: Created `src/dexter/tools/crypto/` directory.
    -   `api.py`: Dedicated API handler using `requests` to call Upbit API.
    -   `prices.py`: Implemented `get_crypto_price_snapshot` and `get_crypto_prices` adapted for Upbit endpoints.
    -   `__init__.py`: Exposed new tools.
2.  **Tool Registration**: Updated `src/dexter/tools/__init__.py` to register the new crypto tools.
3.  **Documentation**:
    -   Created `README-crypto.md` (English & Korean) explaining usage with Upbit.
    -   Created `MAINTENANCE.md` guiding upstream sync and conflict resolution.

### Verification
-   Created and ran `verify_upbit.py` to confirm successful data fetching from Upbit.
-   Simulated an upstream merge conflict to verify the maintenance guide.
