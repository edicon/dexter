#!/usr/bin/env python3
"""
Backtesting framework for volatility prediction accuracy.

This script evaluates the historical accuracy of volatility predictions
by simulating predictions at different points in the past and comparing
them with actual outcomes.
"""
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from dexter.tools.crypto.api import call_api
from dexter.tools.crypto.volatility import calculate_volatility_metrics


def fetch_historical_data(ticker: str, days: int = 60) -> pd.DataFrame:
    """
    Fetch historical price data for backtesting.

    Args:
        ticker: Cryptocurrency ticker
        days: Number of days of historical data

    Returns:
        DataFrame with OHLC data
    """
    market = ticker.upper()
    if "-" not in market:
        market = f"KRW-{market}"

    endpoint = "/candles/days"
    params = {"market": market, "count": days}

    try:
        data = call_api(endpoint, params)
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df = df.iloc[::-1].reset_index(drop=True)

        df = df.rename(columns={
            'opening_price': 'open',
            'high_price': 'high',
            'low_price': 'low',
            'trade_price': 'close',
            'candle_date_time_kst': 'timestamp'
        })

        return df[['timestamp', 'open', 'high', 'low', 'close']]

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return pd.DataFrame()


def calculate_actual_volatility(df: pd.DataFrame, forecast_days: int = 7) -> float:
    """
    Calculate actual volatility for a forecast period.

    Args:
        df: DataFrame with price data for the forecast period
        forecast_days: Length of forecast period

    Returns:
        Actual volatility (range-based percentage)
    """
    if len(df) < forecast_days:
        return 0.0

    period_data = df.tail(forecast_days)
    period_high = period_data['high'].max()
    period_low = period_data['low'].min()

    # Range-based volatility as per GEMINI.md
    volatility = ((period_high - period_low) / period_low) * 100

    return volatility


def simulate_prediction(df: pd.DataFrame, prediction_point: int, lookback: int = 30) -> Dict:
    """
    Simulate a volatility prediction at a specific point in time.

    Args:
        df: Full historical DataFrame
        prediction_point: Index where prediction is made
        lookback: Days to look back for prediction

    Returns:
        Prediction results dictionary
    """
    # Data available at prediction time (everything before prediction_point)
    historical_data = df.iloc[:prediction_point+1]

    if len(historical_data) < lookback:
        return {"error": "Insufficient historical data"}

    # Use the last 'lookback' days for prediction
    prediction_data = historical_data.tail(lookback)

    # Calculate recent volatility
    recent_high = prediction_data['high'].max()
    recent_low = prediction_data['low'].min()
    recent_volatility = ((recent_high - recent_low) / recent_low) * 100

    # Simple prediction: assume similar volatility in next 7 days
    # (In reality, this would use the agent's full prediction logic)
    predicted_volatility = recent_volatility

    # Classify prediction
    if predicted_volatility >= 3.0:
        predicted_class = "HIGH"
    elif predicted_volatility >= 1.5:
        predicted_class = "MODERATE"
    else:
        predicted_class = "LOW"

    return {
        "predicted_volatility": predicted_volatility,
        "predicted_class": predicted_class,
        "timestamp": historical_data.iloc[-1]['timestamp']
    }


def run_backtest(ticker: str, total_days: int = 60, forecast_days: int = 7, lookback: int = 30):
    """
    Run backtesting simulation for volatility predictions.

    Args:
        ticker: Cryptocurrency ticker
        total_days: Total historical period to test
        forecast_days: Forecast horizon (default: 7 days)
        lookback: Days to use for making prediction
    """
    print("\n" + "="*80)
    print(f"Volatility Prediction Backtest - {ticker}")
    print("="*80 + "\n")

    print(f"📊 Configuration:")
    print(f"   Total Period: {total_days} days")
    print(f"   Forecast Horizon: {forecast_days} days")
    print(f"   Lookback Period: {lookback} days")
    print()

    # Fetch historical data
    print("📥 Fetching historical data...")
    df = fetch_historical_data(ticker, total_days)

    if df.empty:
        print("❌ Failed to fetch historical data")
        return

    print(f"✅ Fetched {len(df)} days of data")
    print()

    # Run backtesting
    results = []

    # Start predictions from 'lookback + forecast_days' to ensure we have enough data
    start_point = lookback
    end_point = len(df) - forecast_days

    if end_point <= start_point:
        print("❌ Insufficient data for backtesting")
        return

    print(f"🔄 Running {end_point - start_point} simulated predictions...")
    print()

    for i in range(start_point, end_point):
        # Simulate prediction at this point
        prediction = simulate_prediction(df, i, lookback)

        if "error" in prediction:
            continue

        # Calculate actual volatility for next 'forecast_days'
        actual_data = df.iloc[i+1:i+1+forecast_days]
        actual_volatility = calculate_actual_volatility(actual_data, forecast_days)

        # Classify actual volatility
        if actual_volatility >= 3.0:
            actual_class = "HIGH"
        elif actual_volatility >= 1.5:
            actual_class = "MODERATE"
        else:
            actual_class = "LOW"

        # Calculate errors
        error = abs(prediction["predicted_volatility"] - actual_volatility)
        squared_error = error ** 2
        direction_correct = (prediction["predicted_class"] == actual_class)

        results.append({
            "timestamp": prediction["timestamp"],
            "predicted_volatility": prediction["predicted_volatility"],
            "predicted_class": prediction["predicted_class"],
            "actual_volatility": actual_volatility,
            "actual_class": actual_class,
            "error": error,
            "squared_error": squared_error,
            "direction_correct": direction_correct
        })

    if not results:
        print("❌ No predictions generated")
        return

    # Calculate performance metrics
    print(f"✅ Generated {len(results)} predictions\n")

    # Convert to DataFrame for easier analysis
    results_df = pd.DataFrame(results)

    # Calculate metrics
    rmse = np.sqrt(results_df['squared_error'].mean())
    mae = results_df['error'].mean()
    direction_accuracy = results_df['direction_correct'].sum() / len(results_df) * 100

    # Classification-specific accuracy
    class_accuracy = {}
    for class_name in ["HIGH", "MODERATE", "LOW"]:
        class_predictions = results_df[results_df['predicted_class'] == class_name]
        if len(class_predictions) > 0:
            correct = class_predictions['direction_correct'].sum()
            total = len(class_predictions)
            accuracy = (correct / total) * 100
            class_accuracy[class_name] = {
                "correct": correct,
                "total": total,
                "accuracy": accuracy
            }

    # Display results
    print("="*80)
    print("📊 BACKTEST RESULTS")
    print("="*80 + "\n")

    print(f"📈 Period: {results_df.iloc[0]['timestamp'][:10]} to {results_df.iloc[-1]['timestamp'][:10]}")
    print(f"📉 Total Predictions: {len(results_df)}")
    print()

    print("🎯 Performance Metrics:")
    print(f"   RMSE (Root Mean Square Error): {rmse:.2f}%")
    print(f"   MAE (Mean Absolute Error): {mae:.2f}%")
    print(f"   Direction Accuracy: {direction_accuracy:.1f}% ({results_df['direction_correct'].sum()}/{len(results_df)} correct)")
    print()

    print("📊 Classification Accuracy:")
    for class_name in ["HIGH", "MODERATE", "LOW"]:
        if class_name in class_accuracy:
            stats = class_accuracy[class_name]
            print(f"   {class_name}: {stats['accuracy']:.1f}% ({stats['correct']}/{stats['total']})")
    print()

    # Recent predictions showcase
    print("📋 Recent Predictions (Last 5):")
    recent = results_df.tail(5)
    for idx, row in recent.iterrows():
        symbol = "✅" if row['direction_correct'] else "❌"
        print(f"   {symbol} {row['timestamp'][:10]}: Predicted {row['predicted_class']} ({row['predicted_volatility']:.1f}%), "
              f"Actual {row['actual_class']} ({row['actual_volatility']:.1f}%)")
    print()

    # Recommendations
    print("💡 Recommendations:")
    if direction_accuracy >= 75:
        print("   ✅ Model performs well overall")
    elif direction_accuracy >= 60:
        print("   ⚠️  Model shows moderate performance - consider improvements")
    else:
        print("   ❌ Model needs significant improvement")

    if rmse > 5.0:
        print("   ⚠️  High prediction error - predictions may be unreliable")

    for class_name, stats in class_accuracy.items():
        if stats['accuracy'] >= 80:
            print(f"   ✅ Excellent {class_name} volatility detection")
        elif stats['accuracy'] < 60:
            print(f"   ⚠️  Poor {class_name} volatility detection - needs improvement")

    print()
    print("="*80)
    print("Backtest Complete")
    print("="*80)


if __name__ == "__main__":
    # Run backtest for Bitcoin
    run_backtest("BTC", total_days=60, forecast_days=7, lookback=30)
