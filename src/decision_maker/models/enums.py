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


class LogicOp(TextChoices):
    AND = "AND", _("AND")
    OR = "OR", _("OR")
    DISABLED = "DISABLED", _("None")


class AvailableIndicators(TextChoices):
    MM7 = "MM7", _("Moyenne mobile 7")
    MM20 = "MM20", _("Moyenne mobile 20")
    MM50 = "MM50", _("Moyenne mobile 50")
    MM100 = "MM100", _("Moyenne mobile 100")
    MM200 = "MM200", _("Moyenne mobile 200")

    @classmethod
    def from_code(cls, code: str):
        for c_type in cls:
            if c_type.value == code:
                return c_type
        return None

    @property
    def speed(self):
        return 1000 / int(self.name.split("MM")[-1])
