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
from utils.abstract_client import AbstractAPIClient, CryptoWatchAbstractClient
from utils.enums import TimeUnits
from utils.exceptions import NotAvailableException

headers = {"Content-Type": "application/x-www-form-urlencoded"}


@singleton
class KrakenClient(CryptoWatchAbstractClient):
    @dataclass
    class Configuration:
        api_key: str = os.getenv(
            "COINMARKET_API_KEY", "41751faa-b6f0-46c9-8ee3-7a202111ec58"
        )

    PUBLIC_API_VERSION = "v3"
    BASE_URL = "https://api.kraken.com/0/public/OHLC"
    logger = getLogger("django")

    @inject
    def __init__(self, config: Configuration):
        self._api_key = config.api_key

    def get_tradable_pairs(self):
        url = "https://api.kraken.com/0/public/AssetPairs?info=info"

        req = requests.get(url)
        result = req.json().get("result")
        symbols = []
        for symbol, info in result.items():
            symbols.append(
                {
                    "platform": "kraken",
                    "instrument_name": info.get("altname"),
                    "base_currency": info.get("wsname").split("/")[0],
                    "quote_currency": info.get("wsname").split("/")[1],
                }
            )

        return symbols

    def get_quotes(self, symbol: Symbol, time_unit: TimeUnits):
        start = self._get_start_timestamp(symbol, time_unit)
        req = requests.get(
            f"{self.BASE_URL}?pair={symbol.name}&since={start}&interval={time_unit.minutes_interval}",
            headers=headers,
        )
        resp = req.json()
        if resp.get("error") == ["EGeneral:Invalid arguments"]:
            raise NotAvailableException(f"{symbol.name} not found on Kraken")
        else:
            result = resp.get("result")
            result = result.pop(list(result.keys())[0])
            df = self._build_dataframe(result, time_unit)
        try:
            quotes = json.loads(df.to_json(orient="records"))
        except:
            breakpoint()

        return quotes

    def _build_dataframe(self, data: list[list], time_unit: TimeUnits) -> DataFrame:
        df = DataFrame(
            data,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "vwap",
                "volume",
                "count",
            ],
        ).sort_values("timestamp")
        df["timestamp"] = df["timestamp"]
        df["close_time"] = df["timestamp"] + time_unit.minutes_interval * 60 - 1
        return df
