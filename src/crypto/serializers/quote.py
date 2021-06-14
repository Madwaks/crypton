from rest_framework import serializers

from crypto.models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        exclude = ["symbol", "time_unit", "close_time"]
