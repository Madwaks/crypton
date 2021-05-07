from injector import singleton

from crypto.models import Symbol


@singleton
class SymbolFactory:
    def build_symbols(self, symbols_data: list[dict]) -> list[Symbol]:
        return [self.build_symbol(symbol_data) for symbol_data in symbols_data]

    def build_symbol(self, symbol_data: dict) -> Symbol:
        return Symbol(
            name=symbol_data.get("symbol"),
            base_asset=symbol_data.get("base_asset"),
            quote_asset=symbol_data.get("quote_asset"),
            order_types=symbol_data.get("order_types"),
        )
