import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from crypto.models import Quote
from utils.enums import TimeUnits


def get_timestamp_diff_unit(
    quote: "Quote", diff_number: int
) -> datetime.datetime.timestamp:
    time_unit = TimeUnits.from_code(quote.time_unit)
    return str(
        int(
            int(quote.timestamp) / 1000
            - diff_number * time_unit.to_timedelta().total_seconds()
        )
        * 1000
    )


def is_in_tolerance_range(
    base_value: float, ind_value: float, tolerance: float = 0.0001
):
    bound1 = base_value - base_value * tolerance
    bound2 = base_value + base_value * tolerance
    return bound1 < ind_value < bound2
