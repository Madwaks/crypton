from typing import Type, Optional
from typing import TypeVar

from django.conf import settings, LazySettings
from injector import Injector, Binder

T = TypeVar("T")

_injector: Optional[Injector] = None


def _configure_crypto_quots(binder: Binder, settings: LazySettings):
    from crypto.services.repositories.quote_pair import QuotesPairRepository

    binder.bind(
        QuotesPairRepository.Configuration,
        QuotesPairRepository.Configuration(
            file_folder_path=settings.CRYPTO_QUOTES_FOLDER
        ),
    )


def _configure_quotes_storer(binder: Binder, settings: LazySettings):
    from core.utils.download_data.quotes.boursorama import QuotationDownloader

    binder.bind(
        QuotationDownloader.Configuration,
        QuotationDownloader.Configuration(
            quotes_json_folder=settings.QUOTES_FOLDER_PATH
        ),
    )


def _configure(binder: Binder):
    pass

def _create_injector():
    global _injector
    if _injector is None:
        _injector = Injector(_configure)


def provide(clazz: Type[T]) -> T:
    _create_injector()

    return _injector.get(clazz)
