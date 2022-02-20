import json
import multiprocessing
from dataclasses import dataclass
from datetime import datetime
from itertools import repeat
from time import time, sleep

import requests
from dateutil import tz
from injector import singleton, inject
from pandas import DataFrame

from crypto.models import Symbol
from utils.abstract_client import AbstractAPIClient
from utils.enums import TimeUnits
from utils.exceptions import NotAvailableException


@singleton
class CryptowatchClient(AbstractAPIClient):
    @dataclass
    class Config:
        api_key: str = "Q4W1QDTH1F3LZYZG5BOZ"

    @inject
    def __init__(self, config: Config):
        self._config = config
        self.available_markets = ["BINANCE", "BITFINEX", "KRAKEN"]

    def _get_from_cw(self, url: str):
        resp = requests.get(url)
        return resp.json()

    def get_quotes(self, symbol: Symbol, time_unit: TimeUnits):
        start = self._get_start_timestamp(symbol, time_unit)
        cw_period = time_unit.minutes_interval * 60
        url = f"https://api.cryptowat.ch/markets/coinbase-pro/{symbol.name.lower()}/ohlc?after={start}&before={int(time())}&periods={cw_period}"
        pool_obj = multiprocessing.Pool(processes=1)

        try:
            resp = pool_obj.map(self._get_from_cw, repeat(url, times=1))[0]
            sleep(20)
            pool_obj.terminate()

            pool_obj.join()

        except Exception:
            raise NotAvailableException(f"{symbol.name} not found on Coinbase")
        try:
            result = resp.get("result").get(str(cw_period))
            df = self._build_dataframe(result, time_unit)
            quotes = json.loads(df.to_json(orient="records"))
            return quotes
        except Exception:
            raise NotAvailableException(f"{symbol.name} not found on Coinbase")

    def _build_dataframe(self, data: list[list], time_unit: TimeUnits) -> DataFrame:
        df = DataFrame(
            data,
            columns=[
                "close_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "QuoteVolume",
            ],
        ).sort_values("close_time")
        df["timestamp"] = (
            (df.close_time)
            .shift()
            .fillna(df["close_time"][0] - time_unit.minutes_interval * 60)
        )
        df["open_date"] = df["timestamp"].map(
            lambda val: datetime.fromtimestamp(val, tz=tz.tzutc())
        )
        df["close_date"] = (df["close_time"] - 1).map(
            lambda val: datetime.fromtimestamp(val, tz=tz.tzutc())
        )
        return df
