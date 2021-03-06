from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from crypto.models import Quote
from decision_maker.models import Distance


class QuoteDistanceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj: Quote):
        return f"{obj.symbol.name} - {obj.open_date}"

    class Meta:
        model = Quote
        fields = ["name", "close"]


class DistanceSerializer(serializers.ModelSerializer):
    quote = SerializerMethodField()
    symbol = SerializerMethodField()
    time_unit = SerializerMethodField()
    binance_url = SerializerMethodField()

    def get_symbol(self, obj: Distance):
        return f"{obj.quote.symbol}"

    def get_quote(self, obj: Distance):
        return f"{obj.quote.open_date}"

    def get_time_unit(self, obj: Distance):
        return f"{obj.quote.time_unit}"

    def get_binance_url(self, obj: Distance):
        return f"https://www.binance.com/fr/trade/{obj.quote.symbol.name}"

    class Meta:
        model = Distance
        fields = "__all__"
