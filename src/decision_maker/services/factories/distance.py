from typing import NoReturn, Union

from injector import singleton

from crypto.models import Quote, Symbol
from decision_maker.models.distance import Distance
from utils.enums import TimeUnits


@singleton
class DistanceFactory:

    Distance.objects.bulk_save(distances)
