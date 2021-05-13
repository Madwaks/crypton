from django.db import models
from django.utils.translation import gettext_lazy as _


class PositionStatus(models.TextChoices):
    OPENED = "OPEN", _("Opened")
    CLOSED = "CLOSE", _("Closed")


class ReasonClosed(models.TextChoices):
    SL = "STOP", _("StopLoss")
    TP = "TAKE", _("TakeProfit")
    OTHER = "OTHER", _("Other")
