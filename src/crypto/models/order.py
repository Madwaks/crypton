from django.db.models import Model, CharField, OneToOneField, SET_NULL, FloatField

from crypto.utils.enums import OrderType, Side, TimeInForce


class Order(Model):
    order_id = CharField(max_length=256, primary_key=True)
    type: OrderType
    timestamp = CharField(max_length=512)
    symbol = OneToOneField(
        "crypto.symbol",
        related_name="orders",
        null=False,
        blank=False,
        default="ETHBTC",
        on_delete=SET_NULL,
    )
    side = CharField(max_length=64, choices=Side.choices)

    def __str__(self):
        return f"{self.symbol} - {self.type}"


class LimitOrder(Order):
    type = OrderType.LIMIT
    time_in_force = CharField(max_length=64, choices=TimeInForce.choices, default="GTC")
    price = FloatField(default=0.0)
    quantity = FloatField(default=0.0)


class MarketOrder(Order):
    type = OrderType.MARKET
    quote_order_qty = FloatField(default=0.0)

    def post_body(self):
        return {
            "timestamp": self.timestamp,
            "symbol": self.symbol.name,
            "side": self.side,
            "type": self.type,
            "quoteOrderQty": self.quote_order_qty,
        }


class StopOrder(Order):
    stop_price = FloatField(default=0.0)
    quantity = FloatField(default=0.0)
