import math
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from time import sleep
from typing import TYPE_CHECKING, Any

from binance.client import Client
from injector import singleton, inject
from pandas import to_datetime, DataFrame

from crypto.models import Symbol

if TYPE_CHECKING:
    from utils.enums import TimeUnits

logger = getLogger("django")


class BinanceClient(Client):
    PUBLIC_API_VERSION = "v3"

    def get_needed_pair_quotes(
        self, symbol: Symbol, time_unit: "TimeUnits", existing_data: DataFrame
    ):
        oldest_point, newest_point = self._get_minutes_of_new_data(
            symbol.name, time_unit.value, existing_data
        )
        delta_min = (newest_point - oldest_point).total_seconds() / 60
        available_data = math.ceil(delta_min / time_unit.binsize)
        logger.info(
            f"Downloading {delta_min} minutes of new data available for {symbol.name}, i.e. {available_data} instances of {time_unit.value} data."
        )
        if delta_min < 1:
            return
        klines = self.get_historical_klines(
            symbol.name,
            time_unit.value,
            oldest_point.strftime("%d %b %Y %H:%M:%S"),
            newest_point.strftime("%d %b %Y %H:%M:%S"),
        )
        return self._build_dataframe(klines)

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


@singleton
class TestClient(BinanceClient):
    API_URL = "https://testnet.binance.vision/api"

    @dataclass
    class Configuration:
        api_key: str
        secret_key: str

    @inject
    def __init__(self, _config: Configuration):
        super().__init__(
            api_key=_config.api_key, api_secret=_config.secret_key, testnet=True
        )
