from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

if TYPE_CHECKING:
    from core.models import Quote


class CompanyManager(Manager):
    def all(self) -> QuerySet:
        return super(CompanyManager, self).all()

    def resolve_indicator_query(
        self, indicator1: str, operator: str, indicator2: str
    ) -> QuerySet:
        wanted_items = set()

        for company in self.all():
            quote = Quote.objects.get_last_company_quote(company)

            if self._evaluate_expression(
                quote, indicator1=indicator1, operator=operator, indicator2=indicator2
            ):
                wanted_items.add(company.pk)

        return self.filter(pk__in=wanted_items)

    @staticmethod
    def _evaluate_expression(
        quote: "Quote", indicator1: str, indicator2: str, operator: str
    ) -> bool:
        value1 = quote.indicators.get(name=indicator1).value
        value2 = quote.indicators.get(name=indicator2).value
        expression = f"{value1} {operator} {value2}"
        return eval(expression)
