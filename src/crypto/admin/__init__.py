from django.contrib import admin

from crypto.admin.models.quote import QuoteAdmin
from crypto.admin.models.symbol import SymbolAdmin
from crypto.models import Quote, Symbol

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Symbol, SymbolAdmin)
