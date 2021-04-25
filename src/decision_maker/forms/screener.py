from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms

from decision_maker.models import Screener
from utils.layouts.formset_layout import Formset


class ScreenerForm(forms.ModelForm):
    class Meta:
        model = Screener
        exclude = ()

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = True
        helper.form_class = "form-horizontal"
        helper.label_class = "col-md-3 create-label"
        helper.field_class = "col-md-9"
        helper.layout = Layout(
            Div(
                Field("name"),
                Fieldset("Add conditions", Formset("conditions")),
                HTML("<br>"),
                ButtonHolder(Submit("submit", "save")),
            )
        )
        return helper
