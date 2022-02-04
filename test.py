from dataclasses import dataclass

import cryptowatch as cw
from datetime import datetime, timedelta

import injector
from injector import singleton


@singleton
class CryptowatchClient:
    @dataclass
    class Config:
        api_key: str

    @injector.inject
    def __init__(self, config: Config):
        self._config = config
        cw.api_key = self._config.api_key
        self.assets = cw.assets
        self.instruments = cw.instruments
        self.exchanges = cw.exchanges
        self.markets = cw.markets


# Get all Kraken markets
kraken = cw.markets.list("kraken")

# For each Kraken market...
for market in kraken.markets:

    # Forge current market ticker, like KRAKEN:BTCUSD
    ticker = "{}:{}".format(market.exchange, market.pair).upper()
    # Request weekly candles for that market
    candles = cw.markets.get(ticker, ohlc=True, periods=["1w"])

    # Each candle is a list of [close_timestamp, open, high, low, close, volume, volume_quote]
    # Get close_timestamp, open and close from the most recent weekly candle
    close_ts, wkly_open, wkly_close = (
        candles.of_1w[-1][0],
        candles.of_1w[-1][1],
        candles.of_1w[-1][4],
    )

    # Compute market performance, skip if open was 0
    if wkly_open == 0:
        continue
    perf = (wkly_open - wkly_close) * 100 / wkly_open

    # If the market performance was 5% or more, print it
    if perf >= 5:
        open_ts = datetime.utcfromtimestamp(close_ts) - timedelta(days=7)
        print("{} gained {:.2f}% since {}".format(ticker, perf, open_ts))
