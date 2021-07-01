from rest_framework import serializers

from decision_maker.models import Indicator, SymbolIndicator


class IndicatorSerializer(serializers.ModelSerializer):
    timestamp = serializers.CharField(source="quote.timestamp")

    class Meta:
        model = Indicator
        fields = ["name", "value", "timestamp"]


class SymbolIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymbolIndicator
        fields = ["value"]
