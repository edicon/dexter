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

## 2025-11-24: LangSmith Integration

### Summary
Added LangSmith tracing and monitoring support to enable detailed debugging, token usage tracking, and performance analysis.

### Changes
1.  **Documentation**:
    -   Updated `README.md` with LangSmith setup instructions.
    -   Added optional environment variables for LangSmith configuration.

### Benefits
-   **Token Usage Tracking**: Monitor exact token consumption per request.
-   **Execution Tracing**: Visualize agent decision flow and tool calls.
-   **Performance Analysis**: Track latency and identify bottlenecks.
-   **Debugging**: View detailed input/output at each step.

### Verification
-   Tested LangSmith integration with BTC price query.
-   Confirmed traces appear in LangSmith dashboard at `https://smith.langchain.com/o/default/projects/p/dexter`.

## 2025-11-24: Project Configuration

### Summary
Added standard configuration files for AI agent collaboration and project rules.

### Changes
1.  **Configuration**:
    -   `GEMINI.md`: Defined project rules, coding standards, and language preferences (Korean). Added explicit rule to consult `MAINTENANCE.md` for upstream sync.
    -   `AGENTS.md`: Created as a symbolic link to `GEMINI.md` for broader agent compatibility.

