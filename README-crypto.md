# Crypto Tools Usage Guide

This guide explains how to use the cryptocurrency tools in Dexter.

## Overview

The crypto tools allow you to fetch real-time and historical cryptocurrency data using the **Upbit API** (free, no key required).

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

## Integration

These tools are automatically registered in `dexter.tools.TOOLS` and can be used by the Dexter agent.

---

# 암호화폐 도구 사용 가이드

이 가이드는 Dexter에서 암호화폐 도구를 사용하는 방법을 설명합니다.

## 개요

암호화폐 도구를 사용하면 **Upbit API** (무료, 키 필요 없음)를 통해 실시간 및 과거 암호화폐 데이터를 가져올 수 있습니다.

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

## 통합

이 도구들은 `dexter.tools.TOOLS`에 자동으로 등록되며 Dexter 에이전트에서 사용할 수 있습니다.
