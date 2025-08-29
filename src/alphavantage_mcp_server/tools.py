"""
AlphaVantage MCP Server Tools Definition

This module contains the tool definitions and schemas for the AlphaVantage MCP server.
"""

import mcp.types as types
from enum import Enum


class AlphavantageTools(str, Enum):
    """Enumeration of all available AlphaVantage tools."""

    TIME_SERIES_INTRADAY = "time_series_intraday"
    TIME_SERIES_DAILY = "time_series_daily"
    TIME_SERIES_DAILY_ADJUSTED = "time_series_daily_adjusted"
    TIME_SERIES_WEEKLY = "time_series_weekly"
    TIME_SERIES_WEEKLY_ADJUSTED = "time_series_weekly_adjusted"
    TIME_SERIES_MONTHLY = "time_series_monthly"
    TIME_SERIES_MONTHLY_ADJUSTED = "time_series_monthly_adjusted"
    STOCK_QUOTE = "stock_quote"
    REALTIME_BULK_QUOTES = "realtime_bulk_quotes"
    SYMBOL_SEARCH = "symbol_search"
    MARKET_STATUS = "market_status"
    REALTIME_OPTIONS = "realtime_options"
    HISTORICAL_OPTIONS = "historical_options"
    NEWS_SENTIMENT = "news_sentiment"
    TOP_GAINERS_LOSERS = "top_gainers_losers"
    INSIDER_TRANSACTIONS = "insider_transactions"
    ANALYTICS_FIXED_WINDOW = "analytics_fixed_window"
    ANALYTICS_SLIDING_WINDOW = "analytics_sliding_window"
    COMPANY_OVERVIEW = "company_overview"
    ETF_PROFILE = "etf_profile"
    COMPANY_DIVIDENDS = "company_dividends"
    COMPANY_SPLITS = "company_dividends"
    INCOME_STATEMENT = "income_statement"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW = "cash_flow"
    COMPANY_EARNINGS = "company_earnings"
    LISTING_STATUS = "listing_status"
    EARNINGS_CALENDAR = "earnings_calendar"
    EARNINGS_CALL_TRANSCRIPT = "earnings_call_transcript"
    IPO_CALENDAR = "ipo_calendar"
    EXCHANGE_RATE = "exchange_rate"
    FX_INTRADAY = "fx_intraday"
    FX_DAILY = "fx_daily"
    FX_WEEKLY = "fx_weekly"
    FX_MONTHLY = "fx_monthly"
    CRYPTO_INTRADAY = "crypto_intraday"
    DIGITAL_CURRENCY_DAILY = "digital_currency_daily"
    DIGITAL_CURRENCY_WEEKLY = "digital_currency_weekly"
    DIGITAL_CURRENCY_MONTHLY = "digital_currency_monthly"
    WTI_CRUDE_OIL = "wti_crude_oil"
    BRENT_CRUDE_OIL = "brent_crude_oil"
    NATURAL_GAS = "natural_gas"
    COPPER = "copper"
    ALUMINUM = "aluminum"
    WHEAT = "wheat"
    CORN = "corn"
    COTTON = "cotton"
    SUGAR = "sugar"
    COFFEE = "coffee"
    ALL_COMMODITIES = "all_commodities"
    REAL_GDP = "real_gdp"
    REAL_GDP_PER_CAPITA = "real_gdp_per_capita"
    TREASURY_YIELD = "treasury_yield"
    FEDERAL_FUNDS_RATE = "federal_funds_rate"
    CPI = "cpi"
    INFLATION = "inflation"
    RETAIL_SALES = "retail_sales"
    DURABLES = "durables"
    UNEMPLOYMENT = "unemployment"
    NONFARM_PAYROLL = "nonfarm_payroll"
    SMA = "sma"
    EMA = "ema"
    WMA = "wma"
    DEMA = "dema"
    TEMA = "tema"
    TRIMA = "trima"
    KAMA = "kama"
    MAMA = "mama"
    VWAP = "vwap"
    T3 = "t3"
    MACD = "macd"
    MACDEXT = "macdext"
    STOCH = "stoch"
    STOCHF = "stochf"
    RSI = "rsi"
    STOCHRSI = "stochrsi"
    WILLR = "willr"
    ADX = "adx"
    ADXR = "adxr"
    APO = "apo"
    PPO = "ppo"
    MOM = "mom"
    BOP = "bop"
    CCI = "cci"
    CMO = "cmo"
    ROC = "roc"
    ROCR = "rocr"
    AROON = "aroon"
    AROONOSC = "aroonosc"
    MFI = "mfi"
    TRIX = "trix"
    ULTOSC = "ultosc"
    DX = "dx"
    MINUS_DI = "minus_di"
    PLUS_DI = "plus_di"
    MINUS_DM = "minus_dm"
    PLUS_DM = "plus_dm"
    BBANDS = "bbands"
    MIDPOINT = "midpoint"
    MIDPRICE = "midprice"
    SAR = "sar"
    TRANGE = "trange"
    ATR = "atr"
    NATR = "natr"
    AD = "ad"
    ADOSC = "adosc"
    OBV = "obv"
    HT_TRENDLINE = "ht_trendline"
    HT_SINE = "ht_sine"
    HT_TRENDMODE = "ht_trendmode"
    HT_DCPERIOD = "ht_dcperiod"
    HT_DCPHASE = "ht_dcphase"
    HT_PHASOR = "ht_phasor"


def tools_definitions():
    return [
        types.Tool(
            name=AlphavantageTools.STOCK_QUOTE.value,
            description="Fetch a stock quote",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_INTRADAY.value,
            description="Fetch a time series intraday",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "adjusted": {"type": "boolean"},
                    "outputsize": {"type": "string"},
                    "datatype": {"type": "string"},
                    "monthly": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_DAILY.value,
            description="Fetch a time series daily",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "outputsize": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_DAILY_ADJUSTED.value,
            description="Fetch a time series daily adjusted",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "outputsize": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_WEEKLY.value,
            description="Fetch a time series weekly",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_WEEKLY_ADJUSTED.value,
            description="Fetch a time series weekly adjusted",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_MONTHLY.value,
            description="Fetch a time series monthly",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TIME_SERIES_MONTHLY_ADJUSTED.value,
            description="Fetch a time series monthly adjusted",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.REALTIME_BULK_QUOTES.value,
            description="Fetch real time bulk quotes",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {"type": "array"},
                },
                "required": ["symbols"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.SYMBOL_SEARCH.value,
            description="Search endpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["keywords"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MARKET_STATUS.value,
            description="Fetch market status",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name=AlphavantageTools.REALTIME_OPTIONS.value,
            description="Fetch realtime options",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                    "contract": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HISTORICAL_OPTIONS.value,
            description="Fetch historical options",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                    "contract": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.NEWS_SENTIMENT.value,
            description="Fetch news sentiment",
            inputSchema={
                "type": "object",
                "properties": {
                    "tickers": {"type": "array"},
                    "topics": {"type": "string"},
                    "time_from": {"type": "string"},
                    "time_to": {"type": "string"},
                    "sort": {"type": "string"},
                    "limit": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["tickers"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TOP_GAINERS_LOSERS.value,
            description="Fetch top gainers and losers",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name=AlphavantageTools.INSIDER_TRANSACTIONS.value,
            description="Fetch insider transactions",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ANALYTICS_FIXED_WINDOW.value,
            description="Fetch analytics fixed window",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {"type": "array"},
                    "interval": {"type": "string"},
                    "series_range": {"type": "string"},
                    "ohlc": {"type": "string"},
                    "calculations": {"type": "array"},
                },
                "required": ["symbols", "series_range", "interval", "calculations"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ANALYTICS_SLIDING_WINDOW.value,
            description="Fetch analytics sliding window",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {"type": "array"},
                    "interval": {"type": "string"},
                    "series_range": {"type": "string"},
                    "ohlc": {"type": "string"},
                    "window_size": {"type": "number"},
                    "calculations": {"type": "array"},
                },
                "required": [
                    "symbols",
                    "series_range",
                    "interval",
                    "calculations",
                    "window_size",
                ],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COMPANY_OVERVIEW.value,
            description="Fetch company overview",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ETF_PROFILE.value,
            description="Fetch ETF profile",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COMPANY_DIVIDENDS.value,
            description="Fetch company dividends",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COMPANY_SPLITS.value,
            description="Fetch company splits",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.INCOME_STATEMENT.value,
            description="Fetch company income statement",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.BALANCE_SHEET.value,
            description="Fetch company balance sheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.CASH_FLOW.value,
            description="Fetch company cash flow",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COMPANY_EARNINGS.value,
            description="Fetch company earnings",
            inputSchema={
                "type": "object",
                "properties": {"symbol": {"type": "string"}},
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.EARNINGS_CALL_TRANSCRIPT.value,
            description="Fetch the earnings call transcript for a given company in a specific quarter",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "quarter": {"type": "string"},
                },
                "required": ["symbol", "quarter"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.LISTING_STATUS.value,
            description="Fetch listing status",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "date": {"type": "string"},
                    "state": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.EARNINGS_CALENDAR.value,
            description="Fetch company earnings calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "horizon": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.IPO_CALENDAR.value,
            description="Fetch IPO calendar",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name=AlphavantageTools.EXCHANGE_RATE.value,
            description="Fetch exchange rate",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_currency": {"type": "string"},
                    "to_currency": {"type": "string"},
                },
                "required": ["from_currency", "to_currency"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.FX_INTRADAY.value,
            description="Fetch FX intraday",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {"type": "string"},
                    "to_symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "outputsize": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["from_symbol", "to_symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.FX_DAILY.value,
            description="Fetch FX daily",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {"type": "string"},
                    "to_symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                    "outputsize": {"type": "string"},
                },
                "required": ["from_symbol", "to_symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.FX_WEEKLY.value,
            description="Fetch FX weekly",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {"type": "string"},
                    "to_symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["from_symbol", "to_symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.FX_MONTHLY.value,
            description="Fetch FX monthly",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_symbol": {"type": "string"},
                    "to_symbol": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["from_symbol", "to_symbol"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.CRYPTO_INTRADAY.value,
            description="Fetch crypto intraday",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "market": {"type": "string"},
                    "interval": {"type": "string"},
                    "outputsize": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "market", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.DIGITAL_CURRENCY_DAILY.value,
            description="Fetch digital currency daily",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "market": {"type": "string"},
                },
                "required": ["symbol", "market"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.DIGITAL_CURRENCY_WEEKLY.value,
            description="Fetch digital currency weekly",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "market": {"type": "string"},
                },
                "required": ["symbol", "market"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.DIGITAL_CURRENCY_MONTHLY.value,
            description="Fetch digital currency monthly",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "market": {"type": "string"},
                },
                "required": ["symbol", "market"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.WTI_CRUDE_OIL.value,
            description="Fetch WTI crude oil",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.BRENT_CRUDE_OIL.value,
            description="Fetch Brent crude oil",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.NATURAL_GAS.value,
            description="Fetch natural gas",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COPPER.value,
            description="Fetch copper",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ALUMINUM.value,
            description="Fetch aluminum",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.WHEAT.value,
            description="Fetch wheat",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.CORN.value,
            description="Fetch corn",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COTTON.value,
            description="Fetch cotton",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.SUGAR.value,
            description="Fetch sugar",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.COFFEE.value,
            description="Fetch coffee",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ALL_COMMODITIES.value,
            description="Fetch all commodities",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.REAL_GDP.value,
            description="Fetch real GDP",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.REAL_GDP_PER_CAPITA.value,
            description="Fetch real GDP per capita",
            inputSchema={
                "type": "object",
                "properties": {
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TREASURY_YIELD.value,
            description="Fetch treasury yield",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "maturity": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.FEDERAL_FUNDS_RATE.value,
            description="Fetch federal funds rate",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.CPI.value,
            description="Fetch consumer price index",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.INFLATION.value,
            description="Fetch inflation",
            inputSchema={
                "type": "object",
                "properties": {
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.RETAIL_SALES.value,
            description="Fetch retail sales",
            inputSchema={
                "type": "object",
                "properties": {
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.DURABLES.value,
            description="Fetch durables",
            inputSchema={
                "type": "object",
                "properties": {
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.UNEMPLOYMENT.value,
            description="Fetch unemployment",
            inputSchema={
                "type": "object",
                "properties": {
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AlphavantageTools.NONFARM_PAYROLL.value,
            description="Fetch nonfarm payroll",
            inputSchema={
                "type": "object",
                "properties": {
                    "datatype": {"type": "string"},
                },
                "required": [],
            },
        ),
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
                        "default": 100,
                    },
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.EMA.value,
            description="Fetch exponential moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.WMA.value,
            description="Fetch weighted moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.DEMA.value,
            description="Fetch double exponential moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TRIMA.value,
            description="Fetch triangular moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.KAMA.value,
            description="Fetch Kaufman adaptive moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
            },
        ),
        types.Tool(
            name=AlphavantageTools.MAMA.value,
            description="Fetch MESA adaptive moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "fastlimit": {"type": "number"},
                    "slowlimit": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": [
                    "symbol",
                    "interval",
                    "series_type",
                    "fastlimit",
                    "slowlimit",
                ],
            },
        ),
        types.Tool(
            name=AlphavantageTools.VWAP.value,
            description="Fetch volume weighted average price",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.T3.value,
            description="Fetch triple exponential moving average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MACD.value,
            description="Fetch moving average convergence divergence",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "fastperiod": {"type": "number"},
                    "slowperiod": {"type": "number"},
                    "signalperiod": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MACDEXT.value,
            description="Fetch moving average convergence divergence next",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "fastperiod": {"type": "number"},
                    "slowperiod": {"type": "number"},
                    "signalperiod": {"type": "number"},
                    "fastmatype": {"type": "number"},
                    "slowmatype": {"type": "number"},
                    "signalmatype": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.STOCH.value,
            description="Fetch stochastic oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "fastkperiod": {"type": "number"},
                    "slowkperiod": {"type": "number"},
                    "slowdperiod": {"type": "number"},
                    "slowkmatype": {"type": "string"},
                    "slowdmatype": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.STOCHF.value,
            description="Fetch stochastic oscillator fast",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "fastkperiod": {"type": "number"},
                    "fastdperiod": {"type": "number"},
                    "fastdmatype": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.RSI.value,
            description="Fetch relative strength index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.STOCHRSI.value,
            description="Fetch stochastic relative strength index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "fastkperiod": {"type": "number"},
                    "fastdperiod": {"type": "number"},
                    "fastdmatype": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.WILLR.value,
            description="Fetch williams percent range",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ADX.value,
            description="Fetch average directional movement index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ADXR.value,
            description="Fetch average directional movement index rating",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.APO.value,
            description="Fetch absolute price oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "fastperiod": {"type": "number"},
                    "slowperiod": {"type": "number"},
                    "matype": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [
                    "symbol",
                    "interval",
                    "series_type",
                    "fastperiod",
                    "slowperiod",
                ],
            },
        ),
        types.Tool(
            name=AlphavantageTools.PPO.value,
            description="Fetch percentage price oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "fastperiod": {"type": "number"},
                    "slowperiod": {"type": "number"},
                    "matype": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": [
                    "symbol",
                    "interval",
                    "series_type",
                    "fastperiod",
                    "slowperiod",
                ],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MOM.value,
            description="Fetch momentum",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.BOP.value,
            description="Fetch balance of power",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.CCI.value,
            description="Fetch commodity channel index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.CMO.value,
            description="Fetch chande momentum oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ROC.value,
            description="Fetch rate of change",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ROCR.value,
            description="Fetch rate of change ratio",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.AROON.value,
            description="Fetch aroon",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.AROONOSC.value,
            description="Fetch aroon oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MFI.value,
            description="Fetch money flow index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TRIX.value,
            description="Fetch triple exponential average",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ULTOSC.value,
            description="Fetch ultimate oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "timeperiod1": {"type": "number"},
                    "timeperiod2": {"type": "number"},
                    "timeperiod3": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": [
                    "symbol",
                    "interval",
                    "timeperiod1",
                    "timeperiod2",
                    "timeperiod3",
                ],
            },
        ),
        types.Tool(
            name=AlphavantageTools.DX.value,
            description="Fetch directional movement index",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MINUS_DI.value,
            description="Fetch minus directional indicator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.PLUS_DI.value,
            description="Fetch plus directional indicator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MINUS_DM.value,
            description="Fetch minus directional movement",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.PLUS_DM.value,
            description="Fetch plus directional movement",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.BBANDS.value,
            description="Fetch bollinger bands",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "nbdevup": {"type": "number"},
                    "nbdevdn": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": [
                    "symbol",
                    "interval",
                    "time_period",
                    "series_type",
                    "nbdevup",
                    "nbdevdn",
                ],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MIDPOINT.value,
            description="Fetch midpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.MIDPRICE.value,
            description="Fetch midprice",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.SAR.value,
            description="Fetch parabolic sar",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "acceleration": {"type": "number"},
                    "maximum": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.TRANGE.value,
            description="Fetch true range",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ATR.value,
            description="Fetch average true range",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.NATR.value,
            description="Fetch normalized average true range",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "time_period": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "time_period"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.AD.value,
            description="Fetch accumulation/distribution line",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.ADOSC.value,
            description="Fetch accumulation/distribution oscillator",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "fastperiod": {"type": "number"},
                    "slowperiod": {"type": "number"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "fastperiod", "slowperiod"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.OBV.value,
            description="Fetch on balance volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HT_TRENDLINE.value,
            description="Fetch hilbert transform - trendline",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HT_SINE.value,
            description="Fetch hilbert transform - sine wave",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval", "series_type"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HT_TRENDMODE.value,
            description="Fetch hilbert transform - trend mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HT_DCPERIOD.value,
            description="Fetch hilbert transform - dominant cycle period",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "series_type": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HT_DCPHASE.value,
            description="Fetch hilbert transform - dominant cycle phase",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
        types.Tool(
            name=AlphavantageTools.HT_PHASOR.value,
            description="Fetch hilbert transform - phasor components",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "interval": {"type": "string"},
                    "month": {"type": "string"},
                    "datatype": {"type": "string"},
                },
                "required": ["symbol", "interval"],
            },
        ),
    ]
