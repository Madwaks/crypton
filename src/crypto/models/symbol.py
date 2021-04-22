from enum import Enum

from django.contrib.postgres.fields import ArrayField
from django.db.models import Model, CharField, UniqueConstraint



class Statuses(Enum):
    ACTIVE = "TRADING"


class Symbol(Model):
    name = CharField(max_length=20)
    base_asset = CharField(max_length=10)
    quote_asset = CharField(max_length=10)
    order_types = ArrayField(base_field=CharField(max_length=64, null=True), size=10)

    def __str__(self) -> CharField:
        return self.name

    class Meta:
        verbose_name = "CryptoPair"
        verbose_name_plural = "CryptoPairs"
        ordering = ("name", "base_asset", "quote_asset")
        constraints = (
            UniqueConstraint(
                fields=("name", "base_asset", "quote_asset"),
                name="unique_per_symbol_pairs",
            ),
        )
