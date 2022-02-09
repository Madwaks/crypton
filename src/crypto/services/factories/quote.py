from typing import Any

from injector import singleton

from crypto.models import Symbol, Quote
from utils.enums import TimeUnits

QuotePairJSON = dict[str, any]


@singleton
class QuoteFactory:
    def build_quote_for_symbol(
        self, symbol: Symbol, time_unit: TimeUnits, objs: list[dict[str, Any]]
    ) -> list[Quote]:
        return [self.build_quote(obj, symbol, time_unit) for obj in objs]

    def build_quote(self, obj: dict, symbol: Symbol, time_unit: TimeUnits) -> Quote:
        return Quote(
            timestamp=obj.get("timestamp"),
            open=obj.get("open"),
            close=obj.get("close"),
            high=obj.get("high"),
            low=obj.get("low"),
            volume=float(obj.get("volume")),
            close_time=obj.get("close_time"),
            symbol=symbol,
            time_unit=time_unit,
        )
