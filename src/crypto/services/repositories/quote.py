import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from injector import singleton, inject

from crypto.models import Symbol
from django.conf import settings
from utils.enums import TimeUnits


@singleton
class QuotesPairRepository:
    @property
    def json_folder(self) -> Path:
        return settings.CRYPTO_FOLDER_PATH / "json"

    @property
    def csv_folder(self) -> Path:
        return settings.CRYPTO_FOLDER_PATH / "csv"

    @property
    def available_tu(self) -> list[TimeUnits]:
        return [
            TimeUnits.from_code(file_name.name.split("-")[1])
            for file_name in self.json_folder.iterdir()
        ]

    @property
    def available_symbol(self) -> list[str]:
        return Symbol.objects.all().value_list("name")

    def get_symbol_quotes(self, symbol: Symbol, time_unit: TimeUnits) -> list[dict[str, Any]]:
        path_to_file = self._get_file_from_symbol_and_tu(symbol, time_unit)
        objs = json.loads(path_to_file.read_text())
        return objs

    def get_csv_name_for_symbol(self, symbol: Symbol, time_unit: TimeUnits) -> Path:
        file_name = f"{symbol.name}-{time_unit.value}-data"
        return self.csv_folder / f"{file_name}.csv"

    def get_json_name_for_symbol(self, symbol: Symbol, time_unit: TimeUnits) -> Path:
        file_name = f"{symbol.name}-{time_unit.value}-data"
        return self.json_folder / f"{file_name}.json"
