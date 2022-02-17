from django.db.models import Manager


class LastQuoteManager(Manager):
    def get_queryset(self):
        return super(LastQuoteManager, self).get_queryset()
