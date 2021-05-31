from django.db.models import Model, FloatField, OneToOneField, CASCADE


class QuoteState(Model):
    quote = OneToOneField(
        "crypto.Quote",
        related_name="quote_state",
        null=False,
        blank=False,
        on_delete=CASCADE,
    )

    MM7_MM20: bool = ()
    MM7_MM50: bool = FloatField()
    MM7_MM100: bool = FloatField()
    MM7_MM200: bool = FloatField()
    MM7_PRICE: bool = FloatField()
    MM20_MM50: bool = FloatField()
    MM20_MM100: bool = FloatField()
    MM20_MM200: bool = FloatField()
    MM20_PRICE: bool = FloatField()
    MM50_MM100: bool = FloatField()
    MM50_MM200: bool = FloatField()
    MM50_PRICE: bool = FloatField()
    MM100_MM200: bool = FloatField()
    MM100_PRICE: bool = FloatField()
    MM200_PRICE: bool = FloatField()
