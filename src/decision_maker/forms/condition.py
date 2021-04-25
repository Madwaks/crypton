from django import forms
from django.forms import inlineformset_factory

from decision_maker.models import Condition, Screener


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = "__all__"


ConditionFormSet = inlineformset_factory(
    Screener,
    Condition,
    form=ConditionForm,
    fields=["name", "operator", "other_name", "day_number", "condition"],
    extra=4,
    can_delete=True,
)
