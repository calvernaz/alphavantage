import asyncio
import json
import logging

import mcp.server.stdio
import mcp.types as types
import toml
import uvicorn
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.streamable_http import StreamableHTTPServerTransport
from starlette.requests import Request
from starlette.responses import Response

from .oauth import OAuthResourceServer, create_oauth_config_from_env
from .prompts import prompts_definitions
from .tools import AlphavantageTools, tools_definitions
from .telemetry_bootstrap import init_telemetry
from .api import (
    fetch_quote,
    fetch_intraday,
    fetch_time_series_daily,
    fetch_time_series_daily_adjusted,
    fetch_time_series_weekly,
    fetch_time_series_weekly_adjusted,
    fetch_time_series_monthly,
    fetch_time_series_monthly_adjusted,
    fetch_realtime_bulk_quotes,
    search_endpoint,
    fetch_market_status,
    fetch_realtime_options,
    fetch_historical_options,
    fetch_news_sentiment,
    fetch_top_gainer_losers,
    fetch_insider_transactions,
    fetch_analytics_fixed_window,
    fetch_analytics_sliding_window,
    fetch_company_overview,
    company_dividends,
    fetch_etf_profile,
    fetch_company_splits,
    fetch_income_statement,
    fetch_balance_sheet,
    fetch_cash_flow,
    fetch_listing_status,
    fetch_earnings_calendar,
    fetch_ipo_calendar,
    fetch_exchange_rate,
    fetch_fx_intraday,
    fetch_fx_daily,
    fetch_fx_weekly,
    fetch_fx_monthly,
    fetch_digital_currency_intraday,
    fetch_digital_currency_daily,
    fetch_digital_currency_monthly,
    fetch_wti_crude,
    fetch_brent_crude,
    fetch_natural_gas,
    fetch_copper,
    fetch_aluminum,
    fetch_wheat,
    fetch_corn,
    fetch_cotton,
    fetch_sugar,
    fetch_coffee,
    fetch_all_commodities,
    fetch_real_gdp,
    fetch_real_gdp_per_capita,
    fetch_treasury_yield,
    fetch_federal_funds_rate,
    fetch_cpi,
    fetch_inflation,
    fetch_retail_sales,
    fetch_durables,
    fetch_unemployment,
    fetch_nonfarm_payrolls,
    fetch_sma,
    fetch_ema,
    fetch_wma,
    fetch_dema,
    fetch_tema,
    fetch_trima,
    fetch_kama,
    fetch_mama,
    fetch_t3,
    fetch_macd,
    fetch_macdext,
    fetch_stoch,
    fetch_stochf,
    fetch_rsi,
    fetch_stochrsi,
    fetch_willr,
    fetch_adx,
    fetch_adxr,
    fetch_apo,
    fetch_ppo,
    fetch_mom,
    fetch_bop,
    fetch_cci,
    fetch_cmo,
    fetch_roc,
    fetch_rocr,
    fetch_aroon,
    fetch_aroonosc,
    fetch_mfi,
    fetch_trix,
    fetch_ultosc,
    fetch_dx,
    fetch_minus_di,
    fetch_plus_di,
    fetch_minus_dm,
    fetch_plus_dm,
    fetch_bbands,
    fetch_midpoint,
    fetch_midprice,
    fetch_sar,
    fetch_trange,
    fetch_atr,
    fetch_natr,
    fetch_ad,
    fetch_adosc,
    fetch_obv,
    fetch_ht_trendline,
    fetch_ht_sine,
    fetch_ht_trendmode,
    fetch_ht_dcperiod,
    fetch_ht_dcphase,
    fetch_ht_phasor,
    fetch_vwap,
    fetch_earnings,
    fetch_earnings_call_transcript,
)

logger = logging.getLogger(__name__)


server = Server("alphavantage")


@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return prompts_definitions()


@server.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> types.GetPromptResult:
    if name == AlphavantageTools.STOCK_QUOTE.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the stock quote for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_INTRADAY.value:
        symbol = arguments.get("symbol") if arguments else ""
        interval = arguments.get("interval") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series intraday for the symbol {symbol} with interval {interval}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_DAILY.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series daily for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_DAILY_ADJUSTED.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series daily adjusted for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_WEEKLY.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series weekly for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_WEEKLY_ADJUSTED.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series weekly adjusted for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_MONTHLY.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series monthly for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TIME_SERIES_MONTHLY_ADJUSTED.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the time series monthly adjusted for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.REALTIME_BULK_QUOTES.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch real time bulk quotes for the symbols {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.SYMBOL_SEARCH.value:
        keywords = arguments.get("keywords") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Search for symbols with keywords {keywords}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.MARKET_STATUS.value:
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text", text="Fetch the market status"
                    ),
                )
            ],
        )
    if name == AlphavantageTools.REALTIME_OPTIONS.value:
        symbol = arguments.get("symbol") if arguments else ""
        contract = arguments.get("contract") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch real time options for the symbol {symbol} with contract {contract}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.HISTORICAL_OPTIONS.value:
        symbol = arguments.get("symbol") if arguments else ""
        contract = arguments.get("contract") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch historical options for the symbol {symbol} with contract {contract}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.NEWS_SENTIMENT.value:
        tickers = arguments.get("tickers") if arguments else ""
        topics = arguments.get("topics") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch news sentiment for the tickers {tickers} with topics {topics}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.TOP_GAINERS_LOSERS.value:
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text", text="Fetch the top gainers and losers"
                    ),
                )
            ],
        )
    if name == AlphavantageTools.INSIDER_TRANSACTIONS.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch insider transactions for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.ANALYTICS_FIXED_WINDOW.value:
        symbol = arguments.get("symbol") if arguments else ""
        window = arguments.get("window") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch analytics with fixed window for the symbol {symbol} with window {window}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.ANALYTICS_SLIDING_WINDOW.value:
        symbol = arguments.get("symbol") if arguments else ""
        window = arguments.get("window") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch analytics with sliding window for the symbol {symbol} with window {window}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.COMPANY_OVERVIEW.value:
        symbol = arguments.get("symbol") if arguments else ""
        datatype = arguments.get("datatype") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the company overview for the symbol {symbol} with datatype {datatype}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.ETF_PROFILE.value:
        symbol = arguments.get("symbol") if arguments else ""
        datatype = arguments.get("datatype") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the ETF profile for the symbol {symbol} with datatype {datatype}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.COMPANY_DIVIDENDS.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the company dividends for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.COMPANY_SPLITS.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the company split events for the symbol {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.INCOME_STATEMENT.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the annual and quarterly income statements for the company {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.BALANCE_SHEET.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the annual and quarterly balance sheet for the company {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.CASH_FLOW.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the annual and quarterly cash flow for the company {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.COMPANY_EARNINGS.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the annual and quarterly earnings (EPS) for the company {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.LISTING_STATUS.value:
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="Fetch the list of active or delisted US stocks and ETFs",
                    ),
                )
            ]
        )
    if name == AlphavantageTools.EARNINGS_CALENDAR.value:
        symbol = arguments.get("symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the earnings expected in the next 3, 6, or 12 months for the {symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.EARNINGS_CALL_TRANSCRIPT.value:
        symbol = arguments.get("symbol") if arguments else ""
        quarter = arguments.get("quarter") if arguments else "2024Q1"
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the earnings call transcript for the {symbol} for the quarter {quarter}",
                    ),
                )
            ],
        )

    if name == AlphavantageTools.IPO_CALENDAR.value:
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="Fetch list of IPOs expected in the next 3 months",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.EXCHANGE_RATE.value:
        from_currency = arguments.get("from_currency") if arguments else ""
        to_currency = arguments.get("to_currency") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the exchange rate from {from_currency} to {to_currency}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.FX_INTRADAY.value:
        from_symbol = arguments.get("from_symbol") if arguments else ""
        to_symbol = arguments.get("to_symbol") if arguments else ""
        interval = arguments.get("interval") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the intraday exchange rate from {from_symbol} to {to_symbol} with interval {interval}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.FX_DAILY.value:
        from_symbol = arguments.get("from_symbol") if arguments else ""
        to_symbol = arguments.get("to_symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the daily exchange rate from {from_symbol} to {to_symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.FX_WEEKLY.value:
        from_symbol = arguments.get("from_symbol") if arguments else ""
        to_symbol = arguments.get("to_symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the weekly exchange rate from {from_symbol} to {to_symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.FX_MONTHLY.value:
        from_symbol = arguments.get("from_symbol") if arguments else ""
        to_symbol = arguments.get("to_symbol") if arguments else ""
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the monthly exchange rate from {from_symbol} to {to_symbol}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.CRYPTO_INTRADAY.value:
        symbol = arguments.get("symbol") if arguments else ""
        market = arguments.get("market") if arguments else ""
        interval = arguments.get("interval") if arguments else ""

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the intraday crypto data for {symbol} in {market} with interval {interval}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.DIGITAL_CURRENCY_DAILY.value:
        symbol = arguments.get("symbol") if arguments else ""
        market = arguments.get("market") if arguments else ""

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the daily historical time series for a digital currency (e.g., {symbol}) traded on a specific market (e.g., {market})",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.DIGITAL_CURRENCY_WEEKLY.value:
        symbol = arguments.get("symbol") if arguments else ""
        market = arguments.get("market") if arguments else ""

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the weekly historical time series for a digital currency (e.g., {symbol}) traded on a specific market, e.g., {market}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.DIGITAL_CURRENCY_MONTHLY.value:
        symbol = arguments.get("symbol") if arguments else ""
        market = arguments.get("market") if arguments else ""

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the monthly historical time series for a digital currency (e.g., {symbol}) traded on a specific market, e.g., {market}",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.WTI_CRUDE_OIL.value:
        function = arguments.get("function") if arguments else "WTI"
        interval = arguments.get("interval") if arguments else "monthly"
        datatype = arguments.get("datatype") if arguments else "json"

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the West Texas Intermediate ({function}) crude oil prices in daily, weekly, and monthly horizons",
                    ),
                )
            ],
        )

    if name == AlphavantageTools.BRENT_CRUDE_OIL.value:
        function = arguments.get("function") if arguments else "Brent"
        interval = arguments.get("interval") if arguments else "monthly"
        datatype = arguments.get("datatype") if arguments else "json"

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Fetch the {function} crude oil prices in daily, weekly, and monthly horizons",
                    ),
                )
            ],
        )
    if name == AlphavantageTools.NATURAL_GAS.value:
        function = arguments.get("function") if arguments else "NATURAL_GAS"
        interval = arguments.get("interval") if arguments else "monthly"
        datatype = arguments.get("datatype") if arguments else "json"

        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="Fetch the Henry Hub natural gas spot prices in daily, weekly, and monthly horizons.",
                    ),
                )
            ],
        )

    raise ValueError("Prompt implementation not found")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Get all available tool definitions with their schemas.

    Returns:
        List of MCP Tool objects with input schemas
    """
    return tools_definitions()


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    try:
        match name:
            case AlphavantageTools.STOCK_QUOTE.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")
                result = await fetch_quote(symbol, datatype)

            case AlphavantageTools.TIME_SERIES_INTRADAY.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                datatype = arguments.get("datatype", "json")
                adjusted = arguments.get("adjusted", True)
                extended_hours = arguments.get("extended_hours", True)
                outputsize = arguments.get("outputsize", "compact")
                month = arguments.get("month", None)

                result = await fetch_intraday(
                    symbol,
                    interval,
                    datatype,
                    extended_hours,
                    adjusted,
                    outputsize,
                    month,
                )
            case AlphavantageTools.TIME_SERIES_DAILY.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")
                outputsize = arguments.get("outputsize", "compact")

                result = await fetch_time_series_daily(symbol, datatype, outputsize)
            case AlphavantageTools.TIME_SERIES_DAILY_ADJUSTED.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")
                outputsize = arguments.get("outputsize", "compact")

                result = await fetch_time_series_daily_adjusted(
                    symbol, datatype, outputsize
                )
            case AlphavantageTools.TIME_SERIES_WEEKLY.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")

                result = await fetch_time_series_weekly(symbol, datatype)
            case AlphavantageTools.TIME_SERIES_WEEKLY_ADJUSTED.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")

                result = await fetch_time_series_weekly_adjusted(symbol, datatype)
            case AlphavantageTools.TIME_SERIES_MONTHLY.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")

                result = await fetch_time_series_monthly(symbol, datatype)
            case AlphavantageTools.TIME_SERIES_MONTHLY_ADJUSTED.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")

                result = await fetch_time_series_monthly_adjusted(symbol, datatype)

            case AlphavantageTools.REALTIME_BULK_QUOTES.value:
                symbols = arguments.get("symbols")
                if not symbols:
                    raise ValueError("Missing required argument: symbols")

                datatype = arguments.get("datatype", "json")
                result = await fetch_realtime_bulk_quotes(symbols, datatype)

            case AlphavantageTools.SYMBOL_SEARCH.value:
                keywords = arguments.get("keywords")
                if not keywords:
                    raise ValueError("Missing required argument: keywords")

                datatype = arguments.get("datatype", "json")
                result = await search_endpoint(keywords, datatype)

            case AlphavantageTools.MARKET_STATUS.value:
                result = await fetch_market_status()

            case AlphavantageTools.REALTIME_OPTIONS.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")
                contract = arguments.get("contract", "all")
                result = await fetch_realtime_options(symbol, datatype, contract)

            case AlphavantageTools.HISTORICAL_OPTIONS.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                datatype = arguments.get("datatype", "json")
                contract = arguments.get("contract", "all")
                result = await fetch_historical_options(symbol, datatype, contract)

            case AlphavantageTools.NEWS_SENTIMENT.value:
                tickers = arguments.get("tickers", [])
                datatype = arguments.get("datatype", "json")
                topics = arguments.get("topics", None)
                time_from = arguments.get("time_from", None)
                time_to = arguments.get("time_to", None)
                sort = arguments.get("sort", "LATEST")
                limit = arguments.get("limit", 50)

                result = await fetch_news_sentiment(
                    tickers, datatype, topics, time_from, time_to, sort, limit
                )

            case AlphavantageTools.TOP_GAINERS_LOSERS.value:
                result = await fetch_top_gainer_losers()

            case AlphavantageTools.INSIDER_TRANSACTIONS.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_insider_transactions(symbol)

            case AlphavantageTools.ANALYTICS_FIXED_WINDOW.value:
                symbols = arguments.get("symbols")
                interval = arguments.get("interval")
                series_range = arguments.get("series_range")
                ohlc = arguments.get("ohlc", "close")
                calculations = arguments.get("calculations")

                if not symbols or not interval or not series_range or not calculations:
                    raise ValueError(
                        "Missing required arguments: symbols, interval, series_range, calculations"
                    )
                result = await fetch_analytics_fixed_window(
                    symbols, interval, series_range, ohlc, calculations
                )

            case AlphavantageTools.ANALYTICS_SLIDING_WINDOW.value:
                symbols = arguments.get("symbols")
                interval = arguments.get("interval")
                series_range = arguments.get("series_range")
                ohlc = arguments.get("ohlc", "close")
                window_size = arguments.get("window_size")
                calculations = arguments.get("calculations", [])

                if (
                    not symbols
                    or not interval
                    or not series_range
                    or not calculations
                    or not window_size
                ):
                    raise ValueError(
                        "Missing required arguments: symbols, interval, series_range, calculations, window_size"
                    )
                result = await fetch_analytics_sliding_window(
                    symbols, series_range, ohlc, interval, interval, calculations
                )

            case AlphavantageTools.COMPANY_OVERVIEW.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_company_overview(symbol)

            case AlphavantageTools.ETF_PROFILE.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_etf_profile(symbol)

            case AlphavantageTools.COMPANY_DIVIDENDS.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await company_dividends(symbol)

            case AlphavantageTools.COMPANY_SPLITS.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_company_splits(symbol)

            case AlphavantageTools.INCOME_STATEMENT.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_income_statement(symbol)
            case AlphavantageTools.BALANCE_SHEET.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_balance_sheet(symbol)

            case AlphavantageTools.CASH_FLOW.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")

                result = await fetch_cash_flow(symbol)

            case AlphavantageTools.COMPANY_EARNINGS.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")
                result = await fetch_earnings(symbol)

            case AlphavantageTools.LISTING_STATUS.value:
                date = arguments.get("date")
                state = arguments.get("state")
                result = await fetch_listing_status(date, state)

            case AlphavantageTools.EARNINGS_CALENDAR.value:
                symbol = arguments.get("symbol")
                horizon = arguments.get("horizon")

                result = await fetch_earnings_calendar(symbol, horizon)

            case AlphavantageTools.EARNINGS_CALL_TRANSCRIPT.value:
                symbol = arguments.get("symbol")
                quarter = arguments.get("quarter")

                result = await fetch_earnings_call_transcript(symbol, quarter)

            case AlphavantageTools.IPO_CALENDAR.value:
                result = await fetch_ipo_calendar()

            case AlphavantageTools.EXCHANGE_RATE.value:
                from_currency = arguments.get("from_currency")
                to_currency = arguments.get("to_currency")

                if not from_currency or not to_currency:
                    raise ValueError(
                        "Missing required arguments: from_currency, to_currency"
                    )

                result = await fetch_exchange_rate(from_currency, to_currency)

            case AlphavantageTools.FX_INTRADAY.value:
                from_symbol = arguments.get("from_symbol")
                to_symbol = arguments.get("to_symbol")
                interval = arguments.get("interval")
                outputsize = arguments.get("outputsize", "compact")
                datatype = arguments.get("datatype", "json")

                if not from_symbol or not to_symbol or not interval:
                    raise ValueError(
                        "Missing required arguments: from_symbol, to_symbol, interval"
                    )

                result = await fetch_fx_intraday(
                    from_symbol, to_symbol, interval, outputsize, datatype
                )

            case AlphavantageTools.FX_DAILY.value:
                from_symbol = arguments.get("from_symbol")
                to_symbol = arguments.get("to_symbol")
                datatype = arguments.get("datatype", "json")
                outputsize = arguments.get("outputsize", "compact")

                if not from_symbol or not to_symbol:
                    raise ValueError(
                        "Missing required arguments: from_symbol, to_symbol"
                    )

                result = await fetch_fx_daily(
                    from_symbol, to_symbol, datatype, outputsize
                )

            case AlphavantageTools.FX_WEEKLY.value:
                from_symbol = arguments.get("from_symbol")
                to_symbol = arguments.get("to_symbol")
                datatype = arguments.get("datatype", "json")

                if not from_symbol or not to_symbol:
                    raise ValueError(
                        "Missing required arguments: from_symbol, to_symbol"
                    )

                result = await fetch_fx_weekly(from_symbol, to_symbol, datatype)

            case AlphavantageTools.FX_MONTHLY.value:
                from_symbol = arguments.get("from_symbol")
                to_symbol = arguments.get("to_symbol")
                datatype = arguments.get("datatype", "json")

                if not from_symbol or not to_symbol:
                    raise ValueError(
                        "Missing required arguments: from_symbol, to_symbol"
                    )

                result = await fetch_fx_monthly(from_symbol, to_symbol, datatype)

            case AlphavantageTools.CRYPTO_INTRADAY.value:
                symbol = arguments.get("symbol")
                market = arguments.get("market")
                interval = arguments.get("interval")
                outputsize = arguments.get("outputsize", "compact")
                datatype = arguments.get("datatype", "json")

                if not symbol or not market or not interval:
                    raise ValueError(
                        "Missing required arguments: symbol, market, interval"
                    )

                result = await fetch_digital_currency_intraday(
                    symbol, market, interval, datatype, outputsize
                )

            case AlphavantageTools.DIGITAL_CURRENCY_DAILY.value:
                symbol = arguments.get("symbol")
                market = arguments.get("market")

                if not symbol or not market:
                    raise ValueError("Missing required arguments: symbol, market")

                result = await fetch_digital_currency_daily(symbol, market)

            case AlphavantageTools.DIGITAL_CURRENCY_WEEKLY.value:
                symbol = arguments.get("symbol")
                market = arguments.get("market")

                if not symbol or not market:
                    raise ValueError("Missing required arguments: symbol, market")

                result = await fetch_digital_currency_daily(symbol, market)

            case AlphavantageTools.DIGITAL_CURRENCY_MONTHLY.value:
                symbol = arguments.get("symbol")
                market = arguments.get("market")

                if not symbol or not market:
                    raise ValueError("Missing required arguments: symbol, market")

                result = await fetch_digital_currency_monthly(symbol, market)

            case AlphavantageTools.WTI_CRUDE_OIL.value:
                interval = arguments.get("interval", "montHly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_wti_crude(interval, datatype)

            case AlphavantageTools.BRENT_CRUDE_OIL.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_brent_crude(interval, datatype)

            case AlphavantageTools.NATURAL_GAS.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_natural_gas(interval, datatype)

            case AlphavantageTools.COPPER.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_copper(interval, datatype)

            case AlphavantageTools.ALUMINUM.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_aluminum(interval, datatype)

            case AlphavantageTools.WHEAT.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_wheat(interval, datatype)

            case AlphavantageTools.CORN.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_corn(interval, datatype)

            case AlphavantageTools.COTTON.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_cotton(interval, datatype)

            case AlphavantageTools.SUGAR.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_sugar(interval, datatype)

            case AlphavantageTools.COFFEE.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_coffee(interval, datatype)

            case AlphavantageTools.ALL_COMMODITIES.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_all_commodities(interval, datatype)

            case AlphavantageTools.REAL_GDP.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_real_gdp(interval, datatype)

            case AlphavantageTools.REAL_GDP_PER_CAPITA.value:
                datatype = arguments.get("datatype", "json")

                result = await fetch_real_gdp_per_capita(datatype)

            case AlphavantageTools.TREASURY_YIELD.value:
                interval = arguments.get("interval", "monthly")
                maturity = arguments.get("maturity", "10year")
                datatype = arguments.get("datatype", "json")

                result = await fetch_treasury_yield(interval, maturity, datatype)

            case AlphavantageTools.FEDERAL_FUNDS_RATE.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_federal_funds_rate(interval, datatype)

            case AlphavantageTools.CPI.value:
                interval = arguments.get("interval", "monthly")
                datatype = arguments.get("datatype", "json")

                result = await fetch_cpi(interval, datatype)

            case AlphavantageTools.INFLATION.value:
                datatype = arguments.get("datatype", "json")

                result = await fetch_inflation(datatype)

            case AlphavantageTools.RETAIL_SALES.value:
                datatype = arguments.get("datatype", "json")

                result = await fetch_retail_sales(datatype)

            case AlphavantageTools.DURABLES.value:
                datatype = arguments.get("datatype", "json")

                result = await fetch_durables(datatype)

            case AlphavantageTools.UNEMPLOYMENT.value:
                datatype = arguments.get("datatype", "json")

                result = await fetch_unemployment(datatype)

            case AlphavantageTools.NONFARM_PAYROLL.value:
                datatype = arguments.get("datatype", "json")

                result = await fetch_nonfarm_payrolls(datatype)

            case AlphavantageTools.SMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")
                max_data_points = arguments.get("max_data_points", 100)

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_sma(
                    symbol,
                    interval,
                    month,
                    time_period,
                    series_type,
                    datatype,
                    max_data_points,
                )

            case AlphavantageTools.EMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_ema(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.WMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_wma(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.DEMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_dema(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.TEMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_tema(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.TRIMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_trima(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.KAMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_kama(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.MAMA.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                fastlimit = arguments.get("fastlimit")
                slowlimit = arguments.get("slowlimit")
                datatype = arguments.get("datatype", "json")

                if (
                    not symbol
                    or not interval
                    or not series_type
                    or not fastlimit
                    or not slowlimit
                ):
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type, fastlimit, slowlimit"
                    )

                result = await fetch_mama(
                    symbol, interval, month, series_type, fastlimit, slowlimit, datatype
                )

            case AlphavantageTools.VWAP.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_vwap(symbol, interval, month, datatype)

            case AlphavantageTools.T3.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_t3(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.MACD.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                fastperiod = arguments.get("fastperiod", 12)
                slowperiod = arguments.get("slowperiod", 26)
                signalperiod = arguments.get("signalperiod", 9)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_macd(
                    symbol,
                    interval,
                    month,
                    series_type,
                    fastperiod,
                    slowperiod,
                    signalperiod,
                    datatype,
                )
            case AlphavantageTools.MACDEXT.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                fastperiod = arguments.get("fastperiod", 12)
                slowperiod = arguments.get("slowperiod", 26)
                signalperiod = arguments.get("signalperiod", 9)
                fastmatype = arguments.get("fastmatype", 0)
                slowmatype = arguments.get("slowmatype", 0)
                signalmatype = arguments.get("signalmatype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_macdext(
                    symbol,
                    interval,
                    month,
                    series_type,
                    fastperiod,
                    slowperiod,
                    signalperiod,
                    fastmatype,
                    slowmatype,
                    signalmatype,
                    datatype,
                )

            case AlphavantageTools.STOCH.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                fastkperiod = arguments.get("fastkperiod", 5)
                slowkperiod = arguments.get("slowkperiod", 3)
                slowdperiod = arguments.get("slowdperiod", 3)
                slowkmatype = arguments.get("slowkmatype", 0)
                slowdmatype = arguments.get("slowdmatype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_stoch(
                    symbol,
                    interval,
                    month,
                    fastkperiod,
                    slowkperiod,
                    slowdperiod,
                    slowkmatype,
                    slowdmatype,
                    datatype,
                )

            case AlphavantageTools.STOCHF.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                fastkperiod = arguments.get("fastkperiod", 5)
                fastdperiod = arguments.get("fastdperiod", 3)
                fastdmatype = arguments.get("fastdmatype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_stochf(
                    symbol,
                    interval,
                    month,
                    fastkperiod,
                    fastdperiod,
                    fastdmatype,
                    datatype,
                )

            case AlphavantageTools.RSI.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_rsi(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.STOCHRSI.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                series_type = arguments.get("series_type")
                fastkperiod = arguments.get("fastkperiod", 5)
                fastdperiod = arguments.get("fastdperiod", 3)
                fastdmatype = arguments.get("fastdmatype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_stochrsi(
                    symbol,
                    interval,
                    month,
                    time_period,
                    series_type,
                    fastkperiod,
                    fastdperiod,
                    fastdmatype,
                    datatype,
                )

            case AlphavantageTools.WILLR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_willr(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.ADX.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_adx(symbol, interval, month, time_period, datatype)

            case AlphavantageTools.ADXR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_adxr(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.APO.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                fastperiod = arguments.get("fastperiod", 12)
                slowperiod = arguments.get("slowperiod", 26)
                matype = arguments.get("matype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_apo(
                    symbol,
                    interval,
                    month,
                    series_type,
                    fastperiod,
                    slowperiod,
                    matype,
                    datatype,
                )

            case AlphavantageTools.PPO.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                fastperiod = arguments.get("fastperiod", 12)
                slowperiod = arguments.get("slowperiod", 26)
                matype = arguments.get("matype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_ppo(
                    symbol,
                    interval,
                    month,
                    series_type,
                    fastperiod,
                    slowperiod,
                    matype,
                    datatype,
                )

            case AlphavantageTools.MOM.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 10)
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_mom(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.BOP.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_bop(symbol, interval, month, datatype)

            case AlphavantageTools.CCI.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 20)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_cci(symbol, interval, month, time_period, datatype)

            case AlphavantageTools.CMO.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_cmo(symbol, interval, month, time_period, datatype)

            case AlphavantageTools.ROC.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 10)
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_roc(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.ROCR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 10)
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_rocr(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.AROON.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_aroon(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.AROONOSC.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_aroonosc(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.MFI.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_mfi(symbol, interval, month, time_period, datatype)

            case AlphavantageTools.TRIX.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 30)
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_trix(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.ULTOSC.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period1 = arguments.get("time_period1", 7)
                time_period2 = arguments.get("time_period2", 14)
                time_period3 = arguments.get("time_period3", 28)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_ultosc(
                    symbol,
                    interval,
                    month,
                    time_period1,
                    time_period2,
                    time_period3,
                    datatype,
                )

            case AlphavantageTools.DX.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_dx(symbol, interval, month, time_period, datatype)

            case AlphavantageTools.MINUS_DI.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_minus_di(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.PLUS_DI.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_plus_di(
                    symbol, interval, month, time_period, datatype
                )
            case AlphavantageTools.MINUS_DM.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_minus_dm(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.PLUS_DM.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_plus_dm(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.BBANDS.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 20)
                series_type = arguments.get("series_type")
                nbdevup = arguments.get("nbdevup", 2)
                nbdevdn = arguments.get("nbdevdn", 2)
                matype = arguments.get("matype", 0)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_bbands(
                    symbol,
                    interval,
                    month,
                    time_period,
                    series_type,
                    nbdevup,
                    nbdevdn,
                    matype,
                    datatype,
                )

            case AlphavantageTools.MIDPOINT.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period, series_type"
                    )

                result = await fetch_midpoint(
                    symbol, interval, month, time_period, series_type, datatype
                )

            case AlphavantageTools.MIDPRICE.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_midprice(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.SAR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                acceleration = arguments.get("acceleration", 0.02)
                maximum = arguments.get("maximum", 0.2)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_sar(
                    symbol, interval, month, acceleration, maximum, datatype
                )

            case AlphavantageTools.TRANGE.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_trange(symbol, interval, month, datatype)

            case AlphavantageTools.ATR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_atr(symbol, interval, month, time_period, datatype)

            case AlphavantageTools.NATR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                time_period = arguments.get("time_period", 14)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not time_period:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, time_period"
                    )

                result = await fetch_natr(
                    symbol, interval, month, time_period, datatype
                )

            case AlphavantageTools.AD.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_ad(symbol, interval, month, datatype)

            case AlphavantageTools.ADOSC.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                fastperiod = arguments.get("fastperiod", 3)
                slowperiod = arguments.get("slowperiod", 10)
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_adosc(
                    symbol, interval, month, fastperiod, slowperiod, datatype
                )

            case AlphavantageTools.OBV.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_obv(symbol, interval, month, datatype)

            case AlphavantageTools.HT_TRENDLINE.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_ht_trendline(
                    symbol, interval, month, series_type, datatype
                )

            case AlphavantageTools.HT_SINE.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_type = arguments.get("series_type")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_type:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_type"
                    )

                result = await fetch_ht_sine(
                    symbol, interval, month, series_type, datatype
                )

            case AlphavantageTools.HT_TRENDMODE.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval:
                    raise ValueError("Missing required arguments: symbol, interval")

                result = await fetch_ht_trendmode(symbol, interval, month, datatype)

            case AlphavantageTools.HT_DCPERIOD.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_types = arguments.get("series_types")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_types:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_types"
                    )

                result = await fetch_ht_dcperiod(
                    symbol, interval, month, series_types, datatype
                )

            case AlphavantageTools.HT_DCPHASE.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_types = arguments.get("series_types")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_types:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_types"
                    )

                result = await fetch_ht_dcphase(
                    symbol, interval, month, series_types, datatype
                )

            case AlphavantageTools.HT_PHASOR.value:
                symbol = arguments.get("symbol")
                interval = arguments.get("interval")
                month = arguments.get("month")
                series_types = arguments.get("series_types")
                datatype = arguments.get("datatype", "json")

                if not symbol or not interval or not series_types:
                    raise ValueError(
                        "Missing required arguments: symbol, interval, series_types"
                    )

                result = await fetch_ht_phasor(
                    symbol, interval, month, series_types, datatype
                )
            case _:
                raise ValueError(f"Unknown tool: {name}")

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        raise ValueError(f"Error processing alphavantage query: {str(e)}") from e


def get_version():
    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)
        return pyproject["project"]["version"]


async def run_stdio_server():
    """Run the MCP stdio server"""
    # Initialize telemetry for stdio transport
    init_telemetry(start_metrics=True)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alphavantage",
                server_version=get_version(),
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


async def run_streamable_http_server(port=8080, oauth_enabled=False):
    """Run the Streamable HTTP server on the specified port"""

    # Initialize telemetry for HTTP transport
    init_telemetry(start_metrics=True)

    transport = StreamableHTTPServerTransport(
        mcp_session_id=None, is_json_response_enabled=True
    )

    # Setup OAuth if enabled
    oauth_server = None
    if oauth_enabled:
        oauth_config = create_oauth_config_from_env()
        if oauth_config:
            oauth_server = OAuthResourceServer(oauth_config)
            logger.info(
                f"OAuth enabled for resource server: {oauth_config.resource_server_uri}"
            )
        else:
            logger.warning(
                "OAuth requested but no configuration found. Running without OAuth."
            )

    async with transport.connect() as (read_stream, write_stream):
        server_task = asyncio.create_task(
            server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="alphavantage",
                    server_version=get_version(),
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
        )

        # Create OAuth-enhanced ASGI app wrapper for the transport
        async def asgi_app(scope, receive, send):
            if scope["type"] != "http":
                return await send_404(send)

            path = scope["path"]
            request = Request(scope, receive)

            # Handle OAuth metadata endpoint if OAuth is enabled
            if oauth_server and path == oauth_server.config.resource_metadata_path:
                response = await oauth_server.handle_resource_metadata_request(request)
                return await send_starlette_response(response, send)

            # Handle MCP requests
            elif path.startswith("/mcp"):
                # OAuth authentication if enabled
                if oauth_server:
                    # Extract session ID from request if present
                    session_id = request.headers.get("X-Session-ID")

                    (
                        is_authenticated,
                        validation_result,
                    ) = await oauth_server.authenticate_request(request, session_id)

                    if not is_authenticated:
                        # Return appropriate error response
                        if (
                            validation_result
                            and validation_result.error == "Insufficient scopes"
                        ):
                            response = await oauth_server.create_forbidden_response(
                                error="insufficient_scope",
                                description="Required scopes not present in token",
                            )
                        else:
                            error_desc = (
                                validation_result.error
                                if validation_result
                                else "No valid token provided"
                            )
                            response = await oauth_server.create_unauthorized_response(
                                error="invalid_token", description=error_desc
                            )
                        return await send_starlette_response(response, send)

                    # Log successful authentication
                    logger.info(
                        f"Authenticated MCP request for user: {validation_result.subject}"
                    )

                # Process MCP request
                try:
                    await transport.handle_request(scope, receive, send)
                except Exception as e:
                    logger.error(f"Error handling MCP request: {e}")
                    await send_error_response(send, 500, "Internal Server Error")

            else:
                # Return 404 for unknown paths
                await send_404(send)

        config = uvicorn.Config(asgi_app, host="localhost", port=port)
        uvicorn_server = uvicorn.Server(config)
        http_task = asyncio.create_task(uvicorn_server.serve())

        try:
            await asyncio.gather(server_task, http_task)
        finally:
            # Cleanup OAuth resources
            if oauth_server:
                await oauth_server.cleanup()


async def send_starlette_response(response: Response, send):
    """Send a Starlette Response through ASGI send callable."""
    await send(
        {
            "type": "http.response.start",
            "status": response.status_code,
            "headers": [
                [key.encode(), value.encode()]
                for key, value in response.headers.items()
            ],
        }
    )

    # Handle different response types
    if hasattr(response, "body"):
        body = response.body
    elif hasattr(response, "content"):
        body = response.content
    else:
        body = b""

    await send(
        {
            "type": "http.response.body",
            "body": body,
        }
    )


async def send_404(send):
    """Send a 404 Not Found response."""
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"Not Found",
        }
    )


async def send_error_response(send, status_code: int, message: str):
    """Send an error response."""
    await send(
        {
            "type": "http.response.start",
            "status": status_code,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": message.encode(),
        }
    )


async def main(server_type="stdio", port=8080, oauth_enabled=False):
    """Main entry point with server type selection"""
    if server_type == "http":
        if oauth_enabled:
            logger.info(f"Starting Streamable HTTP server with OAuth on port {port}")
        else:
            logger.info(f"Starting Streamable HTTP server on port {port}")
        await run_streamable_http_server(port=port, oauth_enabled=oauth_enabled)
    else:
        logger.info("Starting stdio server")
        await run_stdio_server()
