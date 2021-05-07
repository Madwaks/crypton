from typing import Any

from crypto.services.factories.symbol import SymbolFactory


def test_symbol_factory_build_symbol(
    symbol_factory: SymbolFactory, mock_symbols_json: list[dict[str, Any]]
):
    symbols = symbol_factory.build_symbols(mock_symbols_json)

    assert len(symbols) == 4

    symbol = symbols[0]

    assert symbol.name == "ETHBTC"
    assert symbol.base_asset == "ETH"
    assert symbol.quote_asset == "BTC"
    assert symbol.order_types == [
        "LIMIT",
        "LIMIT_MAKER",
        "MARKET",
        "STOP_LOSS_LIMIT",
        "TAKE_PROFIT_LIMIT",
    ]
