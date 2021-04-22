from typing import Union

from injector import singleton, inject

from crypto.models import Symbol
from crypton import settings


@singleton
class SymbolRepository:
	@inject
	def __init__(self):
		pass

	@property
	def json_file_path(self):
		return settings.CRYPTO_FOLDER_PATH / "pair.json"

	def get_symbol_from_code(self, symbol: Union[Symbol, str]) -> Symbol:
		if isinstance(symbol, Symbol):
			return symbol
		return Symbol.objects.get(name=symbol)
