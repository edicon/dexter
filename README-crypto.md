# Crypto Tools Usage Guide

This guide explains how to use the cryptocurrency tools in Dexter.

## Overview

The crypto tools allow you to fetch real-time and historical cryptocurrency data, calculate technical indicators, and measure volatility using the **Upbit API** (free, no key required).

## Prerequisites

None. The Upbit API is public.

## Available Tools

### 1. `get_crypto_price_snapshot`

Fetches the latest price data for a specific cryptocurrency.

**Parameters:**
- `ticker`: The symbol of the cryptocurrency (e.g., "BTC", "KRW-BTC"). Defaults to KRW market.

**Example Usage (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_price_snapshot

snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
print(snapshot)
```

### 2. `get_crypto_prices`

Retrieves historical price candles.

**Parameters:**
- `ticker`: The symbol of the cryptocurrency.
- `interval`: Time interval ("minute", "day", "week", "month").
- `interval_multiplier`: Multiplier for minutes (1, 3, 5, 10, 15, 30, 60, 240).
- `count`: Number of candles to retrieve (default: 20).
- `to`: Last candle time (optional).

**Example Usage (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_prices

prices = get_crypto_prices.invoke({
    "ticker": "ETH",
    "interval": "day",
    "count": 7
})
print(prices)
```

### 3. `calculate_technical_indicators` ⭐ NEW

Calculate technical indicators for cryptocurrency analysis.

**Parameters:**
- `ticker`: Cryptocurrency ticker symbol (e.g., "BTC", "ETH")
- `indicators`: List of indicators to calculate ["atr", "rsi", "macd", "bollinger"]
- `period`: Period for calculations (default: 14)
- `data_count`: Number of candles to fetch (default: 100)

**Indicators:**
- **ATR (Average True Range)**: Measures market volatility
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions (0-100)
- **MACD**: Shows trend direction and momentum
- **Bollinger Bands**: Indicates volatility and price levels

**Example Usage (Python):**
```python
from dexter.tools.crypto.indicators import calculate_technical_indicators

indicators = calculate_technical_indicators.invoke({
    "ticker": "BTC",
    "indicators": ["atr", "rsi", "macd", "bollinger"],
    "period": 14
})
print(indicators)
```

**Example Output:**
```json
{
  "ticker": "BTC",
  "period": 14,
  "indicators": {
    "atr": {
      "value": 5097143,
      "percent": 3.92,
      "interpretation": "HIGH volatility"
    },
    "rsi": {
      "value": 38.03,
      "interpretation": "Approaching oversold"
    },
    "macd": {
      "macd_line": -5574269,
      "signal_line": -6224104,
      "histogram": 649834,
      "interpretation": "Bullish momentum"
    },
    "bollinger": {
      "upper": 139542522,
      "middle": 132620500,
      "lower": 125698478,
      "bandwidth": 10.44,
      "interpretation": "HIGH volatility. Price is within normal range."
    }
  }
}
```

### 4. `calculate_volatility_metrics` ⭐ NEW

Calculate cryptocurrency volatility using multiple methods.

**Parameters:**
- `ticker`: Cryptocurrency ticker symbol
- `period`: Number of days for calculation (default: 30)
- `methods`: List of calculation methods ["std", "range", "parkinson", "garman_klass"]

**Volatility Methods:**
- **Standard Deviation**: Classic volatility measure based on returns
- **Range-based**: Uses high-low range (GEMINI.md method)
- **Parkinson's**: Efficient estimator using only high/low prices
- **Garman-Klass**: Advanced estimator using all OHLC prices

**Example Usage (Python):**
```python
from dexter.tools.crypto.volatility import calculate_volatility_metrics

volatility = calculate_volatility_metrics.invoke({
    "ticker": "BTC",
    "period": 30,
    "methods": ["std", "range", "parkinson", "garman_klass"]
})
print(volatility)
```

**Example Output:**
```json
{
  "ticker": "BTC",
  "period": 30,
  "volatility_metrics": {
    "standard_deviation": {
      "daily": 2.27,
      "annualized": 43.43,
      "classification": "MODERATE"
    },
    "range_based": {
      "value": 35.14,
      "max_daily_range": 9.13,
      "avg_daily_range": 4.13,
      "classification": "HIGH"
    },
    "parkinson": {
      "value": 2.67,
      "annualized": 51.05,
      "classification": "MODERATE"
    },
    "garman_klass": {
      "value": 2.78,
      "annualized": 53.04,
      "classification": "MODERATE"
    }
  },
  "comparison": "Methods indicate MODERATE volatility",
  "classification_breakdown": {
    "HIGH": 1,
    "MODERATE": 3,
    "LOW": 0
  }
}
```

## Integration

These tools are automatically registered in `dexter.tools.TOOLS` and can be used by the Dexter agent.

## Scripts

### Testing Scripts

```bash
# Test technical indicators
uv run python src/dexter/tools/crypto/test_crypto_indicators.py

# Test volatility metrics
uv run python src/dexter/tools/crypto/test_volatility.py
```

### Backtesting

```bash
# Run volatility prediction backtest
uv run python scripts/backtest_volatility.py
```

### Volatility Prediction

```bash
# Predict BTC volatility for next 7 days
uv run python scripts/predict_btc_volatility.py

# Verify actual volatility
uv run python scripts/verify_volatility.py
```

---

# 암호화폐 도구 사용 가이드

이 가이드는 Dexter에서 암호화폐 도구를 사용하는 방법을 설명합니다.

## 개요

암호화폐 도구를 사용하면 **Upbit API** (무료, 키 필요 없음)를 통해 실시간 및 과거 암호화폐 데이터를 가져오고, 기술적 지표를 계산하며, 변동성을 측정할 수 있습니다.

## 사전 요구 사항

없음. Upbit API는 공개되어 있습니다.

## 사용 가능한 도구

### 1. `get_crypto_price_snapshot`

특정 암호화폐의 최신 가격 데이터를 가져옵니다.

**매개변수:**
- `ticker`: 암호화폐 심볼 (예: "BTC", "KRW-BTC"). 기본값은 KRW 마켓입니다.

**사용 예시 (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_price_snapshot

snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
print(snapshot)
```

### 2. `get_crypto_prices`

과거 가격 캔들 데이터를 검색합니다.

**매개변수:**
- `ticker`: 암호화폐 심볼.
- `interval`: 시간 간격 ("minute", "day", "week", "month").
- `interval_multiplier`: 분 단위 승수 (1, 3, 5, 10, 15, 30, 60, 240).
- `count`: 가져올 캔들 개수 (기본값: 20).
- `to`: 마지막 캔들 시간 (선택 사항).

**사용 예시 (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_prices

prices = get_crypto_prices.invoke({
    "ticker": "ETH",
    "interval": "day",
    "count": 7
})
print(prices)
```

### 3. `calculate_technical_indicators` ⭐ 신규

암호화폐 분석을 위한 기술적 지표를 계산합니다.

**매개변수:**
- `ticker`: 암호화폐 심볼 (예: "BTC", "ETH")
- `indicators`: 계산할 지표 목록 ["atr", "rsi", "macd", "bollinger"]
- `period`: 계산 기간 (기본값: 14)
- `data_count`: 가져올 캔들 개수 (기본값: 100)

**지표:**
- **ATR (Average True Range)**: 시장 변동성 측정
- **RSI (Relative Strength Index)**: 과매수/과매도 상태 식별 (0-100)
- **MACD**: 추세 방향 및 모멘텀 표시
- **Bollinger Bands**: 변동성 및 가격 수준 표시

**사용 예시 (Python):**
```python
from dexter.tools.crypto.indicators import calculate_technical_indicators

indicators = calculate_technical_indicators.invoke({
    "ticker": "BTC",
    "indicators": ["atr", "rsi", "macd", "bollinger"],
    "period": 14
})
print(indicators)
```

### 4. `calculate_volatility_metrics` ⭐ 신규

여러 방법을 사용하여 암호화폐 변동성을 계산합니다.

**매개변수:**
- `ticker`: 암호화폐 심볼
- `period`: 계산 기간 (일 단위, 기본값: 30)
- `methods`: 계산 방법 목록 ["std", "range", "parkinson", "garman_klass"]

**변동성 계산 방법:**
- **Standard Deviation**: 수익률 기반 고전적 변동성 측정
- **Range-based**: 고가-저가 범위 사용 (GEMINI.md 방법)
- **Parkinson's**: 고가/저가만 사용하는 효율적 추정
- **Garman-Klass**: 모든 OHLC 가격을 사용하는 고급 추정

**사용 예시 (Python):**
```python
from dexter.tools.crypto.volatility import calculate_volatility_metrics

volatility = calculate_volatility_metrics.invoke({
    "ticker": "BTC",
    "period": 30,
    "methods": ["std", "range", "parkinson", "garman_klass"]
})
print(volatility)
```

## 통합

이 도구들은 `dexter.tools.TOOLS`에 자동으로 등록되며 Dexter 에이전트에서 사용할 수 있습니다.

## 스크립트

### 테스트 스크립트

```bash
# 기술적 지표 테스트
uv run python src/dexter/tools/crypto/test_crypto_indicators.py

# 변동성 메트릭 테스트
uv run python src/dexter/tools/crypto/test_volatility.py
```

### 백테스팅

```bash
# 변동성 예측 백테스트 실행
uv run python scripts/backtest_volatility.py
```

### 변동성 예측

```bash
# BTC 향후 7일 변동성 예측
uv run python scripts/predict_btc_volatility.py

# 실제 변동성 검증
uv run python scripts/verify_volatility.py
```

