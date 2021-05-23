from typing import Type, Optional
from typing import TypeVar

from django.conf import settings, LazySettings
from injector import Injector, Binder, ClassAssistedBuilder

from crypto.services.repositories.pair import SymbolRepository
from crypto.services.repositories.quote import QuotesPairRepository

T = TypeVar("T")

_injector: Optional[Injector] = None


def _configure_quotes_repository(binder: Binder, settings: LazySettings):

    binder.bind(
        QuotesPairRepository.Configuration,
        QuotesPairRepository.Configuration(
            json_folder=settings.CRYPTO_FOLDER_PATH / "json",
            csv_folder=settings.CRYPTO_FOLDER_PATH / "csv",
        ),
    )


def _configure_symbol_repository(binder: Binder, settings: LazySettings):

    binder.bind(
        SymbolRepository.Configuration,
        SymbolRepository.Configuration(
            symbol_json_file=settings.CRYPTO_FOLDER_PATH / "pair.json"
        ),
    )


def _configure_test_client(binder: Binder, settings: LazySettings):
    from utils.binance_client import TestClient

    binder.bind(
        TestClient.Configuration,
        TestClient.Configuration(
            api_key=settings.TEST_API_KEY, secret_key=settings.TEST_SECRET_KEY
        ),
    )


def _configure(binder: Binder):
    _configure_quotes_repository(binder, settings)
    _configure_symbol_repository(binder, settings)
    _configure_test_client(binder, settings)


def _create_injector():
    global _injector
    if _injector is None:
        _injector = Injector(_configure)


def provide(clazz: Type[T]) -> T:
    _create_injector()

    return _injector.get(clazz)


def build(clazz: Type[T], **kwargs) -> T:
    _create_injector()

    builder: ClassAssistedBuilder = _injector.get(ClassAssistedBuilder[clazz])

    return builder.build(**kwargs)
