from django.db.models import Model, CharField, IntegerField

from crypto.models import Quote
from decision_maker.models.enums import Operator, AvailableIndicators, LogicOp
from decision_maker.utils.etc import get_timestamp_diff_unit


class Condition(Model):
    base_name = CharField(max_length=128, choices=AvailableIndicators.choices)
    operator = CharField(max_length=8, choices=Operator.choices)
    name_to_compare = CharField(max_length=128, choices=AvailableIndicators.choices)
    time_unit_before = IntegerField(default=0)
    condition = CharField(max_length=16, choices=LogicOp.choices)

    def __str__(self):
        return f"{self.base_name} {self.operator} {self.name_to_compare}"

    def is_fulfilled(self, quote: Quote) -> bool:
        base_indicator = quote.indicators.get(name=self.base_name)
        if self.time_unit_before == 0:
            compared_indicator = quote.indicators.get(name=self.name_to_compare)
        else:
            timestamp = get_timestamp_diff_unit(quote, int(self.time_unit_before))
            breakpoint()
            previous_quote = Quote.objects.get(timestamp=quote.timestamp - timestamp)

            compared_indicator = previous_quote.indicators.get(
                name=self.name_to_compare
            )

        return eval(
            f"{base_indicator.value} {self.operator} {compared_indicator.value}"
        )
