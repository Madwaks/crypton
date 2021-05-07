import json
from dataclasses import dataclass
from pathlib import Path
from random import choice
from typing import Union, Any

from injector import singleton, inject

from crypto.models import Symbol


@singleton
class SymbolRepository:
    @dataclass
    class Configuration:
        symbol_json_file: Path

    @inject
    def __init__(self, config: Configuration):
        self._config = config

    def get_symbols_from_file(self) -> list[dict[str, Any]]:
        return json.loads(self._config.symbol_json_file.read_text())

    def get_one_symbol(self):
        return choice(json.loads(self._config.symbol_json_file.read_text()))

    def get_symbol_from_code(self, symbol: Union[Symbol, str]) -> Symbol:
        if isinstance(symbol, Symbol):
            return symbol
        return Symbol.objects.get(name=symbol)
