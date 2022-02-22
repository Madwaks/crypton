import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import time
from logging import getLogger
from time import sleep
from typing import Any

import requests
from binance.client import Client
from dateutil import tz
from injector import inject
from injector import singleton
from pandas import DataFrame, to_datetime

from crypto.models import Symbol
from crypto.utils.etc import open_date, close_date
from utils.abstract_client import AbstractAPIClient
from utils.enums import TimeUnits
from utils.exceptions import NotAvailableException

logger = getLogger("django")


@singleton
class CryptoComClient:
    BASE_URL = "https://api.crypto.com/v2/public"

    @dataclass
    class Configuration:
        api_key: str = os.getenv("CRYPTOCOM_API_KEY")
        api_secret: str = os.getenv("CRYPTOCOM_API_SECRET")

    @inject
    def __init__(self, config: Configuration):
        self._config = config

    def get_available_instruments(self):
        req = requests.get(f"{self.BASE_URL}/get-instruments")
        pairs = req.json().get("result").get("instruments")
        for pair in pairs:
            pair["platform"] = "binance"
        return pairs


# @singleton
# class CryptowatchClient:
#     @dataclass
#     class Config:
#         api_key: str = "Q4W1QDTH1F3LZYZG5BOZ"
#
#     @inject
#     def __init__(self, config: Config):
#         self._config = config
#         cw.api_key = self._config.api_key
#         self.assets = cw.assets
#         self.instruments = cw.instruments
#         self.exchanges = cw.exchanges
#         self.markets = cw.markets
#         self.available_markets = ["BINANCE", "BITFINEX", "KRAKEN"]
#         self._market_list = self.markets.list()
#
#     def get_quotes(self, symbol: Symbol, time_unit: TimeUnits):
#         quotes = getattr(
#             cw.markets.get(f"BINANCE:{symbol.name}", ohlc=True, periods=[time_unit]),
#             f"of_{time_unit}",
#             after=1421445787,
#         )
#         df = DataFrame(
#             quotes,
#             columns=[
#                 "CloseTime",
#                 "OpenPrice",
#                 "HighPrice",
#                 "LowPrice",
#                 "ClosePrice",
#                 "Volume",
#                 "QuoteVolume",
#             ],
#         )


@singleton
class BinanceClient(Client, AbstractAPIClient):
    @dataclass
    class Configuration:
        api_key: str = os.getenv("BINANCE_API_KEY")
        api_secret: str = os.getenv("BINANCE_API_SECRET")

    PUBLIC_API_VERSION = "v3"

    @inject
    def __init__(self, config: Configuration):
        self._config = config

        super(BinanceClient, self).__init__(
            api_key=self._config.api_key, api_secret=self._config.api_secret
        )

    def get_available_symbols(self):
        exchange_info = self.get_exchange_info()
        symbols = [
            {
                "instrument_name": info.get("symbol"),
                "base_currency": info.get("baseAsset"),
                "quote_currency": info.get("quoteAsset"),
            }
            for info in exchange_info.get("symbols")
            if "SPOT" in info.get("permissions")
        ]
        return symbols

    def get_quotes(self, symbol: Symbol, time_unit: TimeUnits):
        start = self._get_start_datetime(symbol, time_unit)
        if start is None:
            return []
        try:
            klines = self.get_historical_klines(
                symbol.name, time_unit.value, start.strftime("%d %b %Y %H:%M:%S")
            )
            if not klines and not symbol.quotes.exists():
                print([symbol.name] * 5)
        except Exception:
            raise NotAvailableException(f"{symbol.name} not found on Binance")
        return [
            {
                "timestamp": int(quote[0] / 1000),
                "open": quote[1],
                "high": quote[2],
                "low": quote[3],
                "close": quote[4],
                "volume": quote[5],
                "close_time": int(quote[6] / 1000),
            }
            for quote in klines
            if int(quote[6] / 1000) < time()
        ]

    def _build_dataframe(self, klines: list[dict[str, Any]]):
        data = DataFrame(
            klines,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_av",
                "trades",
                "tb_base_av",
                "tb_quote_av",
                "ignore",
            ],
        )
        df = data[
            ["timestamp", "open", "high", "low", "close", "volume", "close_time"]
        ].copy()

        df.timestamp = (df.timestamp / 1000).astype(int)

        df.close_time = (df.close_time / 1000).astype(int)

        return df
