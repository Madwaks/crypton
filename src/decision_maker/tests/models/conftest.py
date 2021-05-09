import pytest

from crypto.models import Quote
from crypto.services.factories.quote import QuoteSymbolFactory
from utils.service_provider import provide


class _MockQuoteFactory(QuoteSymbolFactory):
    def build_previous_quote_from_quote(self, quote: Quote, ts_before: int):
        return Quote(
            timestamp=quote.timestamp,
            open=quote.open,
            close=quote.close,
            high=quote.high,
            low=quote.low,
            volume=float(quote.volume),
            close_time=quote.close_time,
            symbol=quote.symbol,
            time_unit=quote.time_unit,
        )


@pytest.fixture(scope="module")
def quote_factory() -> QuoteSymbolFactory:
    return provide(_MockQuoteFactory)
