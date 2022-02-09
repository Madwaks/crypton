from datetime import timedelta
from logging import getLogger
from typing import Union, Any

from injector import singleton, inject

from crypto.models import Symbol, Quote
from crypto.services.factories.quote import QuoteFactory
from crypto.utils.etc import open_date, close_date
from utils.binance_client import BinanceClient
from utils.enums import TimeUnits

logger = getLogger("django")


@singleton
class QuoteImporter:
    @inject
    def __init__(self, quote_factory: QuoteFactory, binance_client: BinanceClient):
        self._quote_factory = quote_factory
        self._binance_client = binance_client

    def import_quotes(self, symbol: Union[str, Symbol], time_unit: TimeUnits):
        symbol = Symbol.objects.get(name=symbol)
        missing_quotes = self._binance_client.get_quotes(symbol, time_unit)

        if missing_quotes:
            filtered_quotes = [
                quote
                for quote in missing_quotes
                if self._should_import_quote(quote, symbol)
            ]
            quotes = self._quote_factory.build_quote_for_symbol(
                symbol, time_unit, filtered_quotes
            )
            self._perform_save(quotes, symbol)

    def _should_import_quote(self, quote: dict[str, Any], symbol: Symbol):
        is_quote_uncomplete = lambda obj: open_date(obj) < close_date(obj) - timedelta(
            hours=3, minutes=58
        )
        quote_already_exists = (
            lambda obj: open_date(obj) == symbol.last_quote.open_date
            if symbol.last_quote
            else False and close_date(obj) == symbol.last_quote.close_date
        )
        return (
            symbol.last_quote is None
            or (is_quote_uncomplete(quote))
            and not quote_already_exists(quote)
        )

    def _perform_save(self, quotes: list[Quote], symbol: Symbol):
        Quote.objects.bulk_create(quotes)
        last_quote = Quote.objects.get_last_pair_quote(symbol)
        symbol.last_quote = last_quote
        symbol.save()
        logger.info(f"Stored {len(quotes)} for {symbol}")
