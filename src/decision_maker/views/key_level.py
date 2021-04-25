import numpy as np
from django.views.generic import ListView

from core.models import Company
from decision_maker.services.factories.key_level import KeyLevelFactory
from utils.service_provider import provide


class KeyLevelView(ListView):
    model = Company
    template_name = "key_level_company_list.html"

    def get_queryset(self):
        companies = super(KeyLevelView, self).get_queryset()
        key_level_factory = provide(KeyLevelFactory)
        selected_companies_pk = []
        for company in companies:
            last_close = company.last_dated_quotation.close
            levels = key_level_factory.build_key_level_for_company(company)
            nearest_level = self._find_nearest(levels, last_close)
            if abs(nearest_level - last_close) < last_close * 0.02:
                selected_companies_pk.append(company.pk)

        return Company.objects.filter(pk__in=selected_companies_pk)

    def _find_nearest_support(self, levels, value):
        array = np.asarray(levels)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    @staticmethod
    def _find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
