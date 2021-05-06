from django.db.models import Model, OneToOneField, SET_NULL, ManyToManyField


class Strategy(Model):
    symbol = OneToOneField("crypto.Symbol", related_name="strategy", on_delete=SET_NULL)

    conditions = ManyToManyField(
        "decision_maker.Condition",
        related_name="strategy",
        max_length=128,
        null=True,
        on_delete=SET_NULL,
    )
