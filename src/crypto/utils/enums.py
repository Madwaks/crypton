from django.db import models
from django.utils.translation import gettext_lazy as _


class Side(models.TextChoices):
    BUY = "BUY", _("Buy")
    SELL = "SELL", _("Sell")


class OrderType(models.TextChoices):
    LIMIT = "LIMIT", _("LIMIT")
    MARKET = "MARKET", _("MARKET")
    STOP_LOSS = "STOP_LOSS", _("STOP_LOSS")
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT", _("STOP_LOSS_LIMIT")
    TAKE_PROFIT = "TAKE_PROFIT", _("TAKE_PROFIT")
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT", _("TAKE_PROFIT_LIMIT")
    LIMIT_MAKER = "LIMIT_MAKER", _("LIMIT_MAKER")


class TimeInForce(models.TextChoices):
    GTC = "GTC", _("Good until cancelled")
    IOC = "IOC", _("Immediate or cancelled")
    FOK = "FOK", _("Fill or Kill")


class ReasonClosed(models.TextChoices):
    SL = "STOP", _("StopLoss")
    TP = "TAKE", _("TakeProfit")
    OTHER = "OTHER", _("Other")
