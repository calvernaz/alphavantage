"""
AlphaVantage MCP Server Prompts Definition

This module contains the prompt definitions and schemas for the AlphaVantage MCP server.
"""

import mcp.types as types
from mcp.types import Prompt

from .tools import AlphavantageTools


def prompts_definitions() -> list[Prompt]:
    return [
        types.Prompt(
            name=AlphavantageTools.STOCK_QUOTE.value,
            description="Fetch the latest price and volume information for a ticker of your choice",
            arguments=[
                types.PromptArgument(
                    name="symbol",
                    description="Stock symbol",
                    required=True,
                ),
                types.PromptArgument(
                    name="datatype",
                    description="Data type (json or csv). Default is json",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_INTRADAY.value,
            description="Fetch current and 20+ years of historical intraday OHLCV time series of the equity specified",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_DAILY.value,
            description="Fetch a time series daily",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_DAILY_ADJUSTED.value,
            description="Fetch a time series daily adjusted",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="outputsize",
                    description="Output size (compact or full)",
                    required=False,
                ),
                types.PromptArgument(
                    name="datatype",
                    description="Data type (json or csv). Default is json",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_WEEKLY.value,
            description="Fetch a time series weekly",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_WEEKLY_ADJUSTED.value,
            description="Fetch a time series weekly adjusted",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_MONTHLY.value,
            description="Fetch a time series monthly",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TIME_SERIES_MONTHLY_ADJUSTED.value,
            description="Fetch a time series monthly adjusted",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.REALTIME_BULK_QUOTES.value,
            description="Fetch real time bulk quotes",
            arguments=[
                types.PromptArgument(
                    name="symbols", description="Stock symbols", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.SYMBOL_SEARCH.value,
            description="Search endpoint",
            arguments=[
                types.PromptArgument(
                    name="keywords", description="Keywords", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MARKET_STATUS.value,
            description="Fetch market status",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.REALTIME_OPTIONS.value,
            description="Fetch realtime options",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HISTORICAL_OPTIONS.value,
            description="Fetch the full historical options chain for a specific symbol on a specific date, covering 15+ years of history",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="date",
                    description="Trading session date (YYYY-MM-DD). or example, date=2017-11-15",
                    required=True,
                ),
                types.PromptArgument(
                    name="datatype",
                    description="Data type (json or csv). Default is json",
                    required=True,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.NEWS_SENTIMENT.value,
            description="Fetch news sentiment",
            arguments=[
                types.PromptArgument(
                    name="tickers", description="Stock tickers", required=False
                ),
                types.PromptArgument(
                    name="options",
                    description="The news topics of your choice",
                    required=False,
                ),
                types.PromptArgument(
                    name="time_from",
                    description="The time range of the news articles you are targeting, time_from=20220410T0130.",
                    required=False,
                ),
                types.PromptArgument(
                    name="time_to",
                    description="The time range of the news articles you are targeting. time_to=20230410T0130",
                    required=False,
                ),
                types.PromptArgument(
                    name="sort",
                    description="Sort by (latest or oldest). Default sort=LATEST",
                    required=False,
                ),
                types.PromptArgument(
                    name="limit",
                    description="Limit the number of news articles returned. Default=50",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TOP_GAINERS_LOSERS.value,
            description="Fetch top gainers and losers",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.INSIDER_TRANSACTIONS.value,
            description="Fetch insider transactions",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ANALYTICS_FIXED_WINDOW.value,
            description="Fetch analytics fixed window",
            arguments=[
                types.PromptArgument(
                    name="symbols", description="Stock symbols", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ANALYTICS_SLIDING_WINDOW.value,
            description="Fetch analytics sliding window",
            arguments=[
                types.PromptArgument(
                    name="symbols", description="Stock symbols", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.COMPANY_OVERVIEW.value,
            description="Fetch the company information, financial ratios, and other key metrics for the equity specified",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ETF_PROFILE.value,
            description="Fetch ETF profile",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.COMPANY_DIVIDENDS.value,
            description="Fetch company dividends",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.COMPANY_SPLITS.value,
            description="Fetch company splits",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.INCOME_STATEMENT.value,
            description="Fetch company income statement",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.BALANCE_SHEET.value,
            description="Fetch company balance sheet",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.CASH_FLOW.value,
            description="Fetch company cash flow",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.LISTING_STATUS.value,
            description="Fetch listing status",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.COMPANY_EARNINGS.value,
            description="This API returns the annual and quarterly earnings (EPS) for the company of interest.",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.EARNINGS_CALENDAR.value,
            description="Fetch company earnings calendar",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.EARNINGS_CALL_TRANSCRIPT.value,
            description="Fetch earnings call transcript",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="quarter",
                    description="Fiscal quarket in the format YYYYQM",
                    required=True,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.IPO_CALENDAR.value,
            description="Fetch IPO calendar",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.EXCHANGE_RATE.value,
            description="Fetch exchange rate",
            arguments=[
                types.PromptArgument(
                    name="from_currency",
                    description="The currency you would like to get the exchange rate for.",
                    required=True,
                ),
                types.PromptArgument(
                    name="to_currency",
                    description="The destination currency for the exchange rate",
                    required=True,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.FX_INTRADAY.value,
            description="Fetch FX intraday",
            arguments=[
                types.PromptArgument(
                    name="from_symbol", description="From symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.FX_DAILY.value,
            description="Fetch FX daily",
            arguments=[
                types.PromptArgument(
                    name="from_symbol", description="From symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.FX_WEEKLY.value,
            description="Fetch FX weekly",
            arguments=[
                types.PromptArgument(
                    name="from_symbol", description="From symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.FX_MONTHLY.value,
            description="Fetch FX monthly",
            arguments=[
                types.PromptArgument(
                    name="from_symbol", description="From symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.CRYPTO_INTRADAY.value,
            description="Fetch intraday time series (timestamp, open, high, low, close, volume) of the cryptocurrency specified",
            arguments=[
                types.PromptArgument(
                    name="symbol",
                    description="The digital/crypto currency",
                    required=True,
                ),
                types.PromptArgument(
                    name="market",
                    description="The exchange market of your choice",
                    required=True,
                ),
                types.PromptArgument(
                    name="interval",
                    description="Time interval between two consecutive data points in the time series. "
                    "The following values are supported: 1min, 5min, 15min, 30min, 60min",
                    required=True,
                ),
                types.PromptArgument(
                    name="datatype",
                    description="Data type (json or csv). Default is json",
                    required=False,
                ),
                types.PromptArgument(
                    name="outputsize",
                    description="Output size (compact or full)",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.DIGITAL_CURRENCY_DAILY.value,
            description="Fetch digital currency daily",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Digital currency symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.DIGITAL_CURRENCY_WEEKLY.value,
            description="Fetch digital currency weekly",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Digital currency symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.DIGITAL_CURRENCY_MONTHLY.value,
            description="Fetch digital currency monthly",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Digital currency symbol", required=True
                )
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.WTI_CRUDE_OIL.value,
            description="Fetch WTI crude oil",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.BRENT_CRUDE_OIL.value,
            description="Fetch Brent crude oil",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.NATURAL_GAS.value,
            description="Fetch natural gas",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.COPPER.value,
            description="Fetch copper",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.ALUMINUM.value,
            description="Fetch aluminum",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.WHEAT.value, description="Fetch wheat", arguments=[]
        ),
        types.Prompt(
            name=AlphavantageTools.CORN.value, description="Fetch corn", arguments=[]
        ),
        types.Prompt(
            name=AlphavantageTools.COTTON.value,
            description="Fetch cotton",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.SUGAR.value, description="Fetch sugar", arguments=[]
        ),
        types.Prompt(
            name=AlphavantageTools.COFFEE.value,
            description="Fetch coffee",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.ALL_COMMODITIES.value,
            description="Fetch all commodities",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.REAL_GDP.value,
            description="Fetch real GDP",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.REAL_GDP_PER_CAPITA.value,
            description="Fetch real GDP per capita",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.TREASURY_YIELD.value,
            description="Fetch treasury yield",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.FEDERAL_FUNDS_RATE.value,
            description="Fetch federal funds rate",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.CPI.value,
            description="Fetch consumer price index",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.INFLATION.value,
            description="Fetch inflation",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.RETAIL_SALES.value,
            description="Fetch retail sales",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.DURABLES.value,
            description="Fetch durables",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.UNEMPLOYMENT.value,
            description="Fetch unemployment",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.NONFARM_PAYROLL.value,
            description="Fetch nonfarm payroll",
            arguments=[],
        ),
        types.Prompt(
            name=AlphavantageTools.SMA.value,
            description="Fetch the simple moving average (SMA) values",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval",
                    description="Time interval between two consecutive data points in the time series. "
                    "The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly",
                    required=True,
                ),
                types.PromptArgument(
                    name="month",
                    description="ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min) for the equity markets.  For example, month=2009-01",
                    required=False,
                ),
                types.PromptArgument(
                    name="time_period",
                    description="Number of data points used to calculate each moving average value. E.g, time_period=60",
                    required=True,
                ),
                types.PromptArgument(
                    name="series_type",
                    description="The desired price type in the time series. Four types are supported: close, open, high, low",
                    required=True,
                ),
                types.PromptArgument(
                    name="datatype",
                    description="Data type (json or csv). Default is json",
                    required=False,
                ),
                types.PromptArgument(
                    name="max_data_points",
                    description="Maximum number of data points to fetch. Default is 100",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.EMA.value,
            description="Fetch the exponential moving average (EMA) values",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval",
                    description="Time interval between two consecutive data points in the time series. "
                    "The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly",
                    required=True,
                ),
                types.PromptArgument(
                    name="month",
                    description="ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min) for the equity markets.  For example, month=2009-01",
                    required=False,
                ),
                types.PromptArgument(
                    name="time_period",
                    description="Number of data points used to calculate each moving average value. E.g, time_period=60",
                    required=True,
                ),
                types.PromptArgument(
                    name="series_type",
                    description="The desired price type in the time series. Four types are supported: close, open, high, low",
                    required=True,
                ),
                types.PromptArgument(
                    name="datatype",
                    description="Data type (json or csv). Default is json",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.WMA.value,
            description="Fetch weighted moving average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.DEMA.value,
            description="Fetch double exponential moving average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TRIMA.value,
            description="Fetch triangular moving average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.KAMA.value,
            description="Fetch Kaufman adaptive moving average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MAMA.value,
            description="Fetch MESA adaptive moving average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
                types.PromptArgument(
                    name="fastlimit", description="Fast limit", required=True
                ),
                types.PromptArgument(
                    name="slowlimit", description="Slow limit", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.T3.value,
            description="Fetch triple exponential moving average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MACD.value,
            description="Fetch moving average convergence divergence",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MACDEXT.value,
            description="Fetch moving average convergence divergence extended",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.STOCH.value,
            description="Fetch stochastic oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.STOCHF.value,
            description="Fetch stochastic oscillator fast",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.RSI.value,
            description="Fetch relative strength index",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.STOCHRSI.value,
            description="Fetch stochastic relative strength index",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.WILLR.value,
            description="Fetch Williams' percent range",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ADX.value,
            description="Fetch average directional movement index",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ADXR.value,
            description="Fetch average directional movement index rating",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.APO.value,
            description="Fetch absolute price oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
                types.PromptArgument(
                    name="fastperiod", description="Fast period", required=True
                ),
                types.PromptArgument(
                    name="slowperiod", description="Slow period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.PPO.value,
            description="Fetch percentage price oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
                types.PromptArgument(
                    name="fastperiod", description="Fast period", required=True
                ),
                types.PromptArgument(
                    name="slowperiod", description="Slow period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MOM.value,
            description="Fetch momentum",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.BOP.value,
            description="Fetch balance of power",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.CCI.value,
            description="Fetch commodity channel index",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.CMO.value,
            description="Fetch Chande momentum oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ROC.value,
            description="Fetch rate of change",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type",
                    description="The desired price type in the time series. Four types are supported: close, open, high, low",
                    required=True,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ROCR.value,
            description="Fetch rate of change ratio",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.AROON.value,
            description="Fetch Aroon",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.AROONOSC.value,
            description="Fetch aroon oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MFI.value,
            description="Fetch money flow index",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TRIX.value,
            description="Fetch triple exponential average",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type",
                    description="The desired price type in the time series. Four types are supported: close, open, high, low",
                    required=True,
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ULTOSC.value,
            description="Fetch ultimate oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="timeperiod1", description="Time period 1", required=True
                ),
                types.PromptArgument(
                    name="timeperiod2", description="Time period 2", required=True
                ),
                types.PromptArgument(
                    name="timeperiod3", description="Time period 3", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.DX.value,
            description="Fetch directional movement index",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MINUS_DI.value,
            description="Fetch minus directional indicator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.PLUS_DI.value,
            description="Fetch plus directional indicator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MINUS_DM.value,
            description="Fetch minus directional movement",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.PLUS_DM.value,
            description="Fetch plus directional movement",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.BBANDS.value,
            description="Fetch Bollinger bands",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
                types.PromptArgument(
                    name="nbdevup", description="Nbdevup", required=True
                ),
                types.PromptArgument(
                    name="nbdevdn", description="Nbdevdn", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MIDPOINT.value,
            description="Fetch midpoint",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.MIDPRICE.value,
            description="Fetch midprice",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.SAR.value,
            description="Fetch parabolic SAR",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.TRANGE.value,
            description="Fetch true range",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ATR.value,
            description="Fetch average true range",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.NATR.value,
            description="Fetch normalized average true range",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="time_period", description="Time period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.AD.value,
            description="Fetch Chaikin A/D line",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.ADOSC.value,
            description="Fetch Chaikin A/D oscillator",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="fastperiod", description="Fast period", required=True
                ),
                types.PromptArgument(
                    name="slowperiod", description="Slow period", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.OBV.value,
            description="Fetch on balance volume",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HT_TRENDLINE.value,
            description="Fetch Hilbert transform - trendline",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HT_SINE.value,
            description="Fetch Hilbert transform - sine wave",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
                types.PromptArgument(
                    name="series_type", description="Series type", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HT_TRENDMODE.value,
            description="Fetch Hilbert transform - trend mode",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HT_DCPERIOD.value,
            description="Fetch Hilbert transform - dominant cycle period",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HT_DCPHASE.value,
            description="Fetch Hilbert transform - dominant cycle phase",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
        types.Prompt(
            name=AlphavantageTools.HT_PHASOR.value,
            description="Fetch Hilbert transform - phasor components",
            arguments=[
                types.PromptArgument(
                    name="symbol", description="Stock symbol", required=True
                ),
                types.PromptArgument(
                    name="interval", description="Interval", required=True
                ),
            ],
        ),
    ]
