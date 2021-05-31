from injector import singleton
from tqdm import tqdm

from crypto.models import Quote
from decision_maker.models.enums import AvailableIndicators
from decision_maker.models.quote_state import QuoteState


@singleton
class QuoteStateFactory:
    def build_states_from_quotes(self, quote_list: list[Quote]) -> list[QuoteState]:
        state_list = []
        for quote in tqdm(quote_list):
            state = self.build_states_from_quote(quote)
            state_list.append(state)
        return state_list

    def build_states_from_quote(self, quote: Quote):
        name_value_mapping = self._build_name_value_mapping(quote)
        quote_state = QuoteState(quote=quote)
        for field in quote_state._meta.fields:
            if field.name in ["id", "quote"]:
                continue
            self._set_quote_state(
                name=field.name,
                name_value_mapping=name_value_mapping,
                quote_state=quote_state,
            )
        return quote_state

    def _build_name_value_mapping(self, quote: Quote):
        name_value_mapping = dict()
        for name in AvailableIndicators:
            if name.lower() == "price":
                name_value_mapping[name] = quote.close
            else:
                ind = quote.indicators.filter(name=name).first()
                if ind:
                    name_value_mapping[name] = ind.value
                else:
                    name_value_mapping[name] = None
        return name_value_mapping

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
    ):
        base_name, sec_name = self._parse_state_field_name(name)

        base_ind_value = name_value_mapping[base_name]
        sec_ind_value = name_value_mapping[sec_name]
        if base_ind_value and sec_ind_value:
            setattr(quote_state, name, base_ind_value - sec_ind_value)
