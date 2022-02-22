from logging import getLogger
from typing import Union, Optional

from injector import singleton, inject

from crypto.models import Symbol, Quote
from crypto.services.factories.quote import QuoteFactory
from utils.binance_client import BinanceClient
from utils.cryptowatch import CryptowatchClient
from utils.kraken import KrakenClient
from utils.enums import TimeUnits
from utils.exceptions import NotAvailableException


@singleton
class QuoteImporter:
    logger = getLogger("django")

    @inject
    def __init__(
        self,
        quote_factory: QuoteFactory,
        binance_client: BinanceClient,
        kraken_client: KrakenClient,
        cw_client: CryptowatchClient,
    ):
        self._quote_factory = quote_factory
        self._binance_client = binance_client
        self._kraken_client = kraken_client
        self._cw_client = cw_client

    def import_all_quotes(self):
        pass

    def import_quotes(self, symbol: Union[str, Symbol], time_unit: TimeUnits):
        symbol = Symbol.objects.get(name=symbol)
        if symbol.is_up_to_date(time_unit):
            self.logger.info(f"{symbol.name} {time_unit.value} is up to date")
        else:
            missing_quotes = self._find_missing_quotes(symbol, time_unit)
            if missing_quotes:
                quotes = self._quote_factory.build_quote_for_symbol(
                    symbol, time_unit, missing_quotes
                )
                self._perform_save(quotes, symbol, time_unit=time_unit)

    def _find_missing_quotes(
        self, symbol: Symbol, time_unit: TimeUnits
    ) -> Optional[list]:
        clients = [self._binance_client, self._kraken_client]
        for client in clients:
            try:
                return client.get_quotes(symbol, time_unit)
            except NotAvailableException as err:
                self.logger.warning(err)

    def _perform_save(self, quotes: list[Quote], symbol: Symbol, time_unit: TimeUnits):
        Quote.objects.bulk_create(quotes)
        symbol.quotes.filter(time_unit=time_unit.value).update(is_last=False)
        last_quote: Quote = symbol.get_last_quote(time_unit=time_unit)
        last_quote.is_last = True
        last_quote.save()
        self.logger.info(f"Last close for {symbol.name} is {last_quote.close_date}")
