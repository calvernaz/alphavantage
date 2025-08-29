"""
Response utilities for handling large API responses and preventing token limit issues.
"""

import json
from typing import Dict, Any


def limit_time_series_response(
    response: Dict[str, Any], max_data_points: int = 100, preserve_metadata: bool = True
) -> Dict[str, Any]:
    """
    Limit the number of data points in a time series response to prevent token limit issues.

    Args:
        response: The full API response from AlphaVantage
        max_data_points: Maximum number of data points to include (default: 100)
        preserve_metadata: Whether to preserve metadata sections (default: True)

    Returns:
        Limited response with reduced data points
    """
    if not isinstance(response, dict):
        return response

    limited_response = {}

    # Preserve metadata sections (they're usually small)
    if preserve_metadata:
        for key, value in response.items():
            if not isinstance(value, dict) or len(value) < 50:
                limited_response[key] = value

    # Find and limit the main time series data section
    time_series_keys = [
        key
        for key in response.keys()
        if any(
            indicator in key.lower()
            for indicator in [
                "time series",
                "technical analysis",
                "sma",
                "ema",
                "rsi",
                "macd",
                "bbands",
                "stoch",
                "adx",
                "aroon",
                "cci",
                "mom",
                "roc",
                "willr",
                "ad",
                "obv",
                "ht_",
                "atr",
                "natr",
                "trix",
                "ultosc",
                "dx",
                "minus_di",
                "plus_di",
                "minus_dm",
                "plus_dm",
                "midpoint",
                "midprice",
                "sar",
                "trange",
                "adosc",
            ]
        )
    ]

    for ts_key in time_series_keys:
        if ts_key in response and isinstance(response[ts_key], dict):
            time_series_data = response[ts_key]

            # Get the most recent data points (sorted by date descending)
            sorted_dates = sorted(time_series_data.keys(), reverse=True)
            limited_dates = sorted_dates[:max_data_points]

            # Create limited time series with only recent data
            limited_time_series = {
                date: time_series_data[date] for date in limited_dates
            }

            limited_response[ts_key] = limited_time_series

            # Add summary info about the limitation
            if len(sorted_dates) > max_data_points:
                limited_response[f"{ts_key}_summary"] = {
                    "total_data_points_available": len(sorted_dates),
                    "data_points_returned": len(limited_dates),
                    "date_range_returned": {
                        "from": min(limited_dates),
                        "to": max(limited_dates),
                    },
                    "note": f"Response limited to {max_data_points} most recent data points to prevent token limit issues",
                }

    return limited_response


def estimate_response_size(response: Any) -> int:
    """
    Estimate the token size of a response (rough approximation).

    Args:
        response: The response to estimate

    Returns:
        Estimated number of tokens
    """
    try:
        json_str = json.dumps(response, indent=2)
        # Rough approximation: 1 token ≈ 4 characters
        return len(json_str) // 4
    except Exception:
        return 0


def should_limit_response(response: Any, max_tokens: int = 15000) -> bool:
    """
    Check if a response should be limited based on estimated token count.

    Args:
        response: The response to check
        max_tokens: Maximum allowed tokens (default: 15000)

    Returns:
        True if response should be limited
    """
    estimated_tokens = estimate_response_size(response)
    return estimated_tokens > max_tokens


def create_response_summary(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a summary of a large response instead of returning the full data.

    Args:
        response: The full response to summarize

    Returns:
        Summary of the response
    """
    summary = {
        "response_type": "summary",
        "reason": "Full response too large, showing summary to prevent token limit issues",
    }

    # Add metadata sections
    for key, value in response.items():
        if not isinstance(value, dict) or len(value) < 10:
            summary[key] = value

    # Summarize large data sections
    for key, value in response.items():
        if isinstance(value, dict) and len(value) >= 10:
            summary[f"{key}_info"] = {
                "data_points": len(value),
                "date_range": {
                    "earliest": min(value.keys()) if value else None,
                    "latest": max(value.keys()) if value else None,
                },
                "sample_fields": list(list(value.values())[0].keys()) if value else [],
                "note": "Use a more specific date range or limit parameter to get actual data",
            }

    return summary
