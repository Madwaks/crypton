import json
from pathlib import Path
from typing import NoReturn

import docker
from injector import singleton, inject

from crypto.models import Symbol
from crypto.services.factories.symbol import SymbolFactory
from crypton import settings


@singleton
class SymbolImporter:
	@inject
	def __init__(self, symbol_factory: SymbolFactory):
		self._symbol_factory = symbol_factory
		pass

	@property
	def json_file_path(self):
		return settings.CRYPTO_FOLDER_PATH / "available_pairs.json"

	def import_all_symbols(self):
		self._download_available_pairs()
		symbols_json = json.loads(self.json_file_path.read_text())
		self._import_symbols(symbols_json)

	def _import_symbols(self, symbols_json: list[dict]):
		symbols = self._symbol_factory.build_symbols(symbols_json)
		Symbol.objects.bulk_create(symbols)


	def _download_available_pairs(self) -> NoReturn:
		client = docker.from_env()
		host_directory = Path("data/").absolute()
		client.containers.run(image="madwaks/crypto-downloader:1.2", command="importsymbols",
		                      volumes={host_directory: {'bind': '/data', 'mode': 'rw'}})