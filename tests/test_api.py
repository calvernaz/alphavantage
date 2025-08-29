import csv
import os
from io import StringIO

import pytest

from alphavantage_mcp_server.api import (
    fetch_earnings_calendar,
    fetch_earnings_call_transcript,
    fetch_sma,
)


@pytest.mark.asyncio
async def test_fetch_earnings_call_transcript():
    """Test fetching earnings call transcript with real API call."""
    data = await fetch_earnings_call_transcript(symbol="IBM", quarter="2024Q1")

    assert isinstance(data, dict), "API should return JSON data as string"

    assert "symbol" in data, "JSON should contain 'symbol' field"
    assert "quarter" in data, "JSON should contain 'quarter' field"
    assert "transcript" in data, "JSON should contain 'transcript' field"

    assert data["symbol"] == "IBM", "Should find IBM data in the response"
    assert data["transcript"], "Transcript should not be empty"

    first_entry = data["transcript"][0]
    required_fields = ["speaker", "title", "content", "sentiment"]
    for field in required_fields:
        assert field in first_entry, f"Field '{field}' missing from transcript entry"

    assert first_entry["content"], "Transcript content should not be empty"


@pytest.mark.asyncio
async def test_fetch_earnings_calendar():
    """Test fetching earnings calendar with real API call."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    result = await fetch_earnings_calendar(symbol="AAPL", horizon="3month")

    assert isinstance(result, str), "API should return CSV data as string"

    # Parse CSV data
    csv_reader = csv.DictReader(StringIO(result))
    rows = list(csv_reader)

    # Basic validation of structure
    assert rows, "CSV should contain at least one row"

    # Check required fields in first row
    first_row = rows[0]
    required_fields = ["symbol", "name", "reportDate"]
    for field in required_fields:
        assert field in first_row, f"Field '{field}' missing from CSV data"

    # Check if we found AAPL data
    apple_entries = [row for row in rows if row["symbol"] == "AAPL"]
    assert apple_entries, "Should find AAPL entries in the response"


@pytest.mark.asyncio
async def test_fetch_sma():
    """Test fetching SMA (Simple Moving Average) with real API call."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    # Test with common parameters that should work
    result = await fetch_sma(
        symbol="AAPL", interval="daily", time_period=20, series_type="close"
    )

    assert isinstance(result, dict), "API should return JSON data as dict"

    # Check for expected structure in SMA response
    assert "Meta Data" in result, "Response should contain 'Meta Data' section"

    # Find the technical analysis key (it varies by indicator)
    tech_analysis_key = None
    for key in result.keys():
        if "Technical Analysis" in key and "SMA" in key:
            tech_analysis_key = key
            break

    assert tech_analysis_key is not None, (
        "Response should contain Technical Analysis section for SMA"
    )

    # Validate metadata
    meta_data = result["Meta Data"]
    assert "1: Symbol" in meta_data, "Meta Data should contain symbol"
    assert "2: Indicator" in meta_data, "Meta Data should contain indicator type"
    assert "3: Last Refreshed" in meta_data, (
        "Meta Data should contain last refreshed date"
    )
    assert "4: Interval" in meta_data, "Meta Data should contain interval"
    assert "5: Time Period" in meta_data, "Meta Data should contain time period"
    assert "6: Series Type" in meta_data, "Meta Data should contain series type"

    assert meta_data["1: Symbol"] == "AAPL", "Symbol should match request"
    assert meta_data["2: Indicator"] == "Simple Moving Average (SMA)", (
        "Indicator should be SMA"
    )
    assert meta_data["4: Interval"] == "daily", "Interval should match request"
    assert meta_data["5: Time Period"] == 20, "Time period should match request"
    assert meta_data["6: Series Type"] == "close", "Series type should match request"

    # Validate technical analysis data
    sma_data = result[tech_analysis_key]
    assert isinstance(sma_data, dict), "SMA data should be a dictionary"
    assert len(sma_data) > 0, "SMA data should contain at least one data point"

    # Check structure of first data point
    first_date = list(sma_data.keys())[0]
    first_data_point = sma_data[first_date]
    assert isinstance(first_data_point, dict), "Each data point should be a dictionary"
    assert "SMA" in first_data_point, "Data point should contain SMA value"

    # Validate that SMA value is numeric
    sma_value = first_data_point["SMA"]
    assert isinstance(sma_value, str), "SMA value should be string (as returned by API)"
    float(sma_value)  # Should not raise exception if valid number


@pytest.mark.asyncio
async def test_fetch_sma_with_month():
    """Test fetching SMA with month parameter for intraday data."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    # Test with intraday interval and month parameter
    result = await fetch_sma(
        symbol="MSFT",
        interval="60min",
        time_period=14,
        series_type="close",
        month="2024-01",
    )

    assert isinstance(result, dict), "API should return JSON data as dict"
    assert "Meta Data" in result, "Response should contain 'Meta Data' section"

    # Validate that month parameter was applied
    meta_data = result["Meta Data"]
    assert "7: Time Zone" in meta_data, "Meta Data should contain time zone"
    assert meta_data["7: Time Zone"] == "US/Eastern", "Time zone should be US/Eastern"


@pytest.mark.asyncio
async def test_fetch_sma_csv_format():
    """Test fetching SMA in CSV format."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    result = await fetch_sma(
        symbol="GOOGL",
        interval="daily",
        time_period=10,
        series_type="close",
        datatype="csv",
    )

    assert isinstance(result, str), "CSV format should return string data"
    assert len(result) > 0, "CSV data should not be empty"

    # Basic CSV validation
    lines = result.strip().split("\n")
    assert len(lines) > 1, "CSV should have header and at least one data row"

    # Check CSV header
    header = lines[0]
    assert "time" in header.lower(), "CSV should contain time column"
    assert "sma" in header.lower(), "CSV should contain SMA column"


@pytest.mark.asyncio
async def test_fetch_sma_with_response_limiting():
    """Test SMA response limiting functionality to prevent token limit issues."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    # Test with a small max_data_points to demonstrate limiting
    result = await fetch_sma(
        symbol="NVDA",
        interval="daily",
        time_period=14,
        series_type="close",
        max_data_points=10,  # Limit to only 10 data points
    )

    assert isinstance(result, dict), "API should return JSON data as dict"
    assert "Meta Data" in result, "Response should contain 'Meta Data' section"

    # Find the technical analysis key
    tech_analysis_key = None
    for key in result.keys():
        if "Technical Analysis" in key and "SMA" in key:
            tech_analysis_key = key
            break

    assert tech_analysis_key is not None, (
        "Response should contain Technical Analysis section for SMA"
    )

    # Check that response was limited
    sma_data = result[tech_analysis_key]
    assert len(sma_data) <= 10, (
        f"Response should be limited to 10 data points, got {len(sma_data)}"
    )

    # Check for summary information if response was limited
    summary_key = f"{tech_analysis_key}_summary"
    if summary_key in result:
        summary = result[summary_key]
        assert "total_data_points_available" in summary, (
            "Summary should show total available data points"
        )
        assert "data_points_returned" in summary, (
            "Summary should show returned data points"
        )
        assert "note" in summary, "Summary should contain explanation note"
        assert summary["data_points_returned"] == len(sma_data), (
            "Summary count should match actual data"
        )

    # Verify dates are in descending order (most recent first)
    dates = list(sma_data.keys())
    sorted_dates = sorted(dates, reverse=True)
    assert dates == sorted_dates, "Data points should be ordered by most recent first"


@pytest.mark.asyncio
async def test_fetch_sma_large_response_handling():
    """Test SMA handling of potentially large responses."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    assert api_key, "ALPHAVANTAGE_API_KEY must be set in environment"

    # Test with default max_data_points (100)
    result = await fetch_sma(
        symbol="AAPL",
        interval="daily",
        time_period=20,
        series_type="close",
        # Using default max_data_points=100
    )

    assert isinstance(result, dict), "API should return JSON data as dict"

    # Find the technical analysis key
    tech_analysis_key = None
    for key in result.keys():
        if "Technical Analysis" in key and "SMA" in key:
            tech_analysis_key = key
            break

    assert tech_analysis_key is not None, (
        "Response should contain Technical Analysis section"
    )

    # Check that response respects the default limit
    sma_data = result[tech_analysis_key]
    assert len(sma_data) <= 100, (
        f"Response should be limited to 100 data points by default, got {len(sma_data)}"
    )

    # Verify all data points have valid SMA values
    for date, data_point in sma_data.items():
        assert "SMA" in data_point, f"Data point for {date} should contain SMA value"
        sma_value = data_point["SMA"]
        assert isinstance(sma_value, str), "SMA value should be string"
        float(sma_value)  # Should not raise exception if valid number
