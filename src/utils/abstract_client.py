from abc import abstractmethod, ABC
from datetime import datetime
from typing import Any, Optional

from pandas import DataFrame

from crypto.models import Symbol
from utils.enums import TimeUnits


class AbstractAPIClient(ABC):
    @abstractmethod
    def get_quotes(self, symbol: Symbol, time_unit: TimeUnits) -> list[dict[str, Any]]:
        pass

    def _get_start_datetime(
        self, symbol: Symbol, time_unit: TimeUnits
    ) -> Optional[datetime]:
        if symbol.quotes.filter(time_unit=time_unit.value).exists():
            if symbol.is_up_to_date(time_unit):
                return None
            last_symbol_quote = symbol.get_last_quote(time_unit)
            start_ = last_symbol_quote.close_date
            if (start_ + time_unit.to_timedelta()) > datetime.utcnow():
                return None
        else:
            start_ = datetime.utcnow() - 3000 * time_unit.to_timedelta()

        return start_

    def _get_start_timestamp(self, symbol: Symbol, time_unit: TimeUnits) -> int:
        start_dt = self._get_start_datetime(symbol, time_unit)
        return int(start_dt.timestamp())


class CryptoWatchAbstractClient(AbstractAPIClient, ABC):
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
