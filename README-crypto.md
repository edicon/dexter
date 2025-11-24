# Crypto Tools Usage Guide

This guide explains how to use the cryptocurrency tools in Dexter.

## Overview

The crypto tools allow you to fetch real-time and historical cryptocurrency data using the Financial Datasets API.

## Prerequisites

Ensure you have the `FINANCIAL_DATASETS_API_KEY` environment variable set.

## Available Tools

### 1. `get_crypto_price_snapshot`

Fetches the latest price data for a specific cryptocurrency.

**Parameters:**
- `ticker`: The symbol of the cryptocurrency (e.g., "BTC", "ETH").

**Example Usage (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_price_snapshot

snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
print(snapshot)
```

### 2. `get_crypto_prices`

Retrieves historical price data over a specified range.

**Parameters:**
- `ticker`: The symbol of the cryptocurrency.
- `interval`: Time interval ("minute", "day", "week", "month", "year").
- `interval_multiplier`: Multiplier for the interval (default: 1).
- `start_date`: Start date (YYYY-MM-DD).
- `end_date`: End date (YYYY-MM-DD).

**Example Usage (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_prices

prices = get_crypto_prices.invoke({
    "ticker": "ETH",
    "interval": "day",
    "start_date": "2023-01-01",
    "end_date": "2023-01-07"
})
print(prices)
```

## Integration

These tools are automatically registered in `dexter.tools.TOOLS` and can be used by the Dexter agent.

---

# 암호화폐 도구 사용 가이드

이 가이드는 Dexter에서 암호화폐 도구를 사용하는 방법을 설명합니다.

## 개요

암호화폐 도구를 사용하면 Financial Datasets API를 통해 실시간 및 과거 암호화폐 데이터를 가져올 수 있습니다.

## 사전 요구 사항

`FINANCIAL_DATASETS_API_KEY` 환경 변수가 설정되어 있는지 확인하십시오.

## 사용 가능한 도구

### 1. `get_crypto_price_snapshot`

특정 암호화폐의 최신 가격 데이터를 가져옵니다.

**매개변수:**
- `ticker`: 암호화폐 심볼 (예: "BTC", "ETH").

**사용 예시 (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_price_snapshot

snapshot = get_crypto_price_snapshot.invoke({"ticker": "BTC"})
print(snapshot)
```

### 2. `get_crypto_prices`

지정된 기간 동안의 과거 가격 데이터를 검색합니다.

**매개변수:**
- `ticker`: 암호화폐 심볼.
- `interval`: 시간 간격 ("minute", "day", "week", "month", "year").
- `interval_multiplier`: 간격 승수 (기본값: 1).
- `start_date`: 시작 날짜 (YYYY-MM-DD).
- `end_date`: 종료 날짜 (YYYY-MM-DD).

**사용 예시 (Python):**
```python
from dexter.tools.crypto.prices import get_crypto_prices

prices = get_crypto_prices.invoke({
    "ticker": "ETH",
    "interval": "day",
    "start_date": "2023-01-01",
    "end_date": "2023-01-07"
})
print(prices)
```

## 통합

이 도구들은 `dexter.tools.TOOLS`에 자동으로 등록되며 Dexter 에이전트에서 사용할 수 있습니다.
