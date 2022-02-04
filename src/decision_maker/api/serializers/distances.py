from rest_framework import serializers

from crypto.models import Quote
from decision_maker.models import Distance


class QuoteDistanceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj: Quote):
        return f"{obj.symbol.name} - {obj.open_date} - {obj.time_unit}"

    class Meta:
        model = Quote
        fields = ["name", "close"]


class DistanceSerializer(serializers.ModelSerializer):
    quote = serializers.SerializerMethodField()
    abs_mm7 = serializers.SerializerMethodField()
    abs_mm20 = serializers.SerializerMethodField()
    abs_mm50 = serializers.SerializerMethodField()
    abs_mm100 = serializers.SerializerMethodField()
    abs_mm200 = serializers.SerializerMethodField()

    def get_quote(self, obj: Quote):
        return (
            f"{obj.quote.symbol.name} - {obj.quote.open_date} - {obj.quote.time_unit}"
        )

    class Meta:
        model = Distance
        exclude = ("id",)
