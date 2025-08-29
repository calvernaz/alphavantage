# Run the server

Set the environment variable `ALPHAVANTAGE_API_KEY` to your Alphavantage API key.

```bash
uv --directory ~/code/alphavantage run alphavantage
```

### Response Limiting Utilities

#### 1. Modify API Functions
Add `max_data_points` parameter to technical indicator functions:

```python
async def fetch_sma(
    symbol: str,
    interval: str = None,
    month: str = None,
    time_period: int = None,
    series_type: str = None,
    datatype: str = "json",
    max_data_points: int = 100,  # NEW PARAMETER
) -> dict[str, str] | str:
```

#### 2. Apply Response Limiting Logic
```python
# In fetch_sma and other technical indicator functions
if datatype == "csv":
    return response.text
    
# For JSON responses, apply response limiting
full_response = response.json()

from .response_utils import limit_time_series_response, should_limit_response

if should_limit_response(full_response):
    return limit_time_series_response(full_response, max_data_points)

return full_response
```

#### 3. Update Tool Definitions
Add `max_data_points` parameter to tool schemas:

```python
types.Tool(
    name=AlphavantageTools.SMA.value,
    description="Fetch simple moving average",
    inputSchema={
        "type": "object",
        "properties": {
            "symbol": {"type": "string"},
            "interval": {"type": "string"},
            "month": {"type": "string"},
            "time_period": {"type": "number"},
            "series_type": {"type": "string"},
            "datatype": {"type": "string"},
            "max_data_points": {
                "type": "number", 
                "description": "Maximum number of data points to return (default: 100)",
                "default": 100
            },
        },
        "required": ["symbol", "interval", "time_period", "series_type"],
    },
),
```

#### 4. Update Tool Handlers
Pass `max_data_points` parameter to API functions:

```python
case AlphavantageTools.SMA.value:
    symbol = arguments.get("symbol")
    interval = arguments.get("interval")
    month = arguments.get("month")
    time_period = arguments.get("time_period")
    series_type = arguments.get("series_type")
    datatype = arguments.get("datatype", "json")
    max_data_points = arguments.get("max_data_points", 100)  # NEW

    if not symbol or not interval or not time_period or not series_type:
        raise ValueError(
            "Missing required arguments: symbol, interval, time_period, series_type"
        )

    result = await fetch_sma(
        symbol, interval, month, time_period, series_type, datatype, max_data_points
    )
```

# Format

```bash
ruff check src/alphavantage_mcp_server/  --fix
```

# Run Tests

```bash
pytest tests/*.py
```

# Versioning

```bash
bumpversion patch
```