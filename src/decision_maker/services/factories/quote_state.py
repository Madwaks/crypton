from injector import singleton

from crypto.models import Quote
from decision_maker.models.enums import AvailableIndicators
from decision_maker.models.quote_state import QuoteState


@singleton
class QuoteStateFactory:
    def build_states_from_quotes(self, quote_list: list[Quote]) -> list[QuoteState]:
        return [self.build_states_from_quote(quote) for quote in quote_list]

    def build_states_from_quote(self, quote: Quote):
        name_value_mapping = {
            name: quote.indicators.get(name=name).value
            if name.lower() != "price"
            else quote.close
            for name in AvailableIndicators.values
        }
        quote_state = QuoteState(quote=quote)
        for field in quote_state._meta.fields():
            if field.name in ["id", "quote"]:
                continue
            self._set_quote_state(
                name=field.name,
                name_value_mapping=name_value_mapping,
                quote_state=quote_state,
            )
        return quote_state

    def _parse_state_field_name(
        self, name: str
    ) -> tuple[AvailableIndicators, AvailableIndicators]:
        base_name = name.split("_")[0]
        sec_name = name.split("_")[1]
        return (
            AvailableIndicators.from_code(base_name),
            AvailableIndicators.from_code(sec_name),
        )

    def _set_quote_state(
        self, name: str, name_value_mapping: dict[str, float], quote_state: QuoteState
    ) -> QuoteState:
        base_name, sec_name = self._parse_state_field_name(name)

        base_ind_value = name_value_mapping[base_name]
        sec_ind_value = name_value_mapping[sec_name]

        setattr(quote_state, name, base_ind_value - sec_ind_value)
