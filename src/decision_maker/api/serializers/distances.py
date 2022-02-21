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
    quote = QuoteDistanceSerializer()

    # def get_quote(self, obj: Distance):
    #     return str(obj.quote)

    class Meta:
        model = Distance
        fields = "__all__"
