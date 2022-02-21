from typing import TYPE_CHECKING

from django.db.models import Manager

if TYPE_CHECKING:
    from crypto.models import Symbol


class LastDistancesManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(quote__is_last=True)
