from logging import getLogger

from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from decision_maker.forms.condition import ConditionFormSet
from decision_maker.forms.screener import ScreenerForm
from decision_maker.models import Screener

logger = getLogger("django")


class ScreenerCreate(CreateView):
    model = Screener
    template_name = "screener_creation.html"
    form_class = ScreenerForm

    def get_context_data(self, **kwargs):
        data = super(ScreenerCreate, self).get_context_data(**kwargs)

        if self.request.POST:
            data["conditions"] = ConditionFormSet(self.request.POST)
        else:
            data["conditions"] = ConditionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context["titles"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(ScreenerCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "mycollections:collection_detail", kwargs={"pk": self.object.pk}
        )


#
#
# class ScreenerSelectionView(FormView):
#     form_class = IndicatorStateFormSet
#     template_name = "screener_selection.html"
#
#     def form_valid(self, form: Form) -> HttpResponse:
#         final_companies: QuerySet = Company.objects.all()
#         start_time = time()
#         for clean_data in form.cleaned_data:
#             indicator1 = clean_data.get("indicator_1")
#             operator = clean_data.get("operator")
#             indicator2 = clean_data.get("indicator_2")
#             condition = clean_data.get("condition")
#             solved_query = Company.objects.resolve_indicator_query(
#                 indicator1=indicator1, operator=operator, indicator2=indicator2
#             )
#             if condition == Condition.AND:
#                 final_companies = final_companies.intersection(solved_query)
#             elif condition == Condition.OR:
#                 final_companies = final_companies.union(solved_query)
#         logger.info(time() - start_time)
#         return HttpResponseRedirect(
#             reverse(
#                 "core:companies",
#                 kwargs={"pks": [company.pk for company in final_companies]},
#             )
#         )


class ScreenerTest(TemplateView):
    template_name = "screener_test.html"
