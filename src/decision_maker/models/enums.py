from enum import Enum
from typing import Union, Optional

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EnumTrend(Enum):
    UP: str = "bullish"
    DOWN: str = "bearish"
    NEUTRAL: str = "neutral"

    @classmethod
    def enum_to_bool(cls, value: Union[str, "EnumTrend"]) -> Optional[bool]:
        if value == cls.UP:
            return True
        elif value == cls.DOWN:
            return False
        return None

    @classmethod
    def sign_to_enum(cls, value: float) -> "EnumTrend":
        if value == -1:
            return cls.UP
        else:
            return cls.DOWN


class Operator(TextChoices):
    GT = ">", _("GREATER THAN")
    LT = "<", _("GREATER THAN")
    LTE = "<=", _("LOWER OR EQUAL")
    EQ = "==", _("EQUAL")
    GTE = ">=", _("GREATER OR EQUAL")


class Condition(TextChoices):
    AND = "AND", _("AND")
    OR = "OR", _("OR")
    DISABLED = "DISABLED", _("None")


class AvailableIndicators(TextChoices):
    MM7 = "MM7", _("Moyenne mobile 7")
    MM20 = "MM20", _("Moyenne mobile 20")
    MM50 = "MM50", _("Moyenne mobile 50")
    MM100 = "MM100", _("Moyenne mobile 100")
    MM200 = "MM200", _("Moyenne mobile 200")
    PRICE = "price", _("Price")
