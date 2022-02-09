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

    def get_abs_mm7(self, obj: Distance):
        return obj.abs_mm7

    def get_abs_mm20(self, obj: Distance):
        return obj.abs_mm_20

    def get_abs_mm50(self, obj: Distance):
        return obj.abs_mm_50

    def get_abs_mm100(self, obj: Distance):
        return obj.abs_mm_100

    def get_abs_mm200(self, obj: Distance):
        return obj.abs_mm_200

    class Meta:
        model = Distance
        fields = [
            "quote",
            "abs_mm7",
            "abs_mm20",
            "abs_mm100",
            "abs_mm50",
            "abs_mm200",
            "support",
            "resistance",
        ]
