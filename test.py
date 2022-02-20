from coinapi_rest_v1.restapi import CoinAPIv1
import datetime, sys

test_key = "1DD55274-239C-4B21-95B3-F097FA57FC2D"

api = CoinAPIv1(test_key)

start_of_2016 = datetime.date(2016, 1, 1).isoformat()
start_of_2022 = datetime.date(2022, 1, 1).isoformat()
ohlcv_historical = api.ohlcv_historical_data(
    "BITSTAMP_SPOT_BTC_USD",
    {"period_id": "15MIN", "time_start": start_of_2016, "time_end": start_of_2022},
)
breakpoint()
