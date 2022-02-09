import json
import os
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from time import sleep
from typing import Any

import requests
from binance.client import Client
from injector import inject
from injector import singleton
from pandas import DataFrame, to_datetime

from crypto.models import Symbol
from utils.enums import TimeUnits

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
        return req.json().get("result").get("instruments")


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
class BinanceClient(Client):
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

    def get_quotes(self, symbol: Symbol, time_unit: TimeUnits):
        date = datetime.strptime("1 Jan 2017", "%d %b %Y")
        start = symbol.last_quote.open_date if symbol.last_quote else date
        try:
            klines = self.get_historical_klines(
                symbol.name, time_unit.value, start.strftime("%d %b %Y %H:%M:%S")
            )
            quotes = json.loads(self._build_dataframe(klines).to_json(orient="records"))
            if start == date:
                return quotes if len(quotes) > 1000 else []
            else:
                return quotes
        except Exception:
            logger.warning(f"{symbol.name} not found on Binance")

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
        return data

    def _get_minutes_of_new_data(
        self, symbol: str, time_unit: "TimeUnits", data: DataFrame
    ):
        if len(data) > 0:
            old = datetime.fromtimestamp(data["timestamp"].iloc[-1] / 1000)
        else:
            old = datetime.strptime("1 Jan 2017", "%d %b %Y")
        new = to_datetime(
            self.get_klines(symbol=symbol, interval=time_unit)[-1][0], unit="ms"
        )
        sleep(0.5)
        return old, new
