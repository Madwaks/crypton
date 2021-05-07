import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from injector import singleton, inject

from crypto.models import Symbol
from utils.enums import TimeUnits


@singleton
class QuotesPairRepository:
    @dataclass
    class Configuration:
        json_folder: Path
        csv_folder: Path

    @inject
    def __init__(self, config: Configuration):
        self._config = config

    @property
    def available_tu(self) -> list[TimeUnits]:
        return [
            TimeUnits.from_code(file_name.name.split("-")[1])
            for file_name in self.json_folder.iterdir()
        ]

    @property
    def available_symbol(self) -> list[str]:
        return Symbol.objects.all().value_list("name")

    def get_symbol_quotes(
        self, symbol: Symbol, time_unit: TimeUnits
    ) -> list[dict[str, Any]]:
        path_to_file = self.get_json_path_for_symbol(symbol, time_unit)
        objs = json.loads(path_to_file.read_text())
        return objs

    def get_csv_path_for_symbol(self, symbol: Symbol, time_unit: TimeUnits) -> Path:
        return (
            self._config.csv_folder / f"{self._build_file_name(symbol, time_unit)}.csv"
        )

    def get_json_path_for_symbol(self, symbol: Symbol, time_unit: TimeUnits) -> Path:
        return (
            self._config.json_folder
            / f"{self._build_file_name(symbol, time_unit)}.json"
        )

    def _build_file_name(self, symbol: Symbol, time_unit: TimeUnits):
        return f"{symbol.name}-{time_unit.value}-data"
