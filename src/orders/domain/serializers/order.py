import json
from typing import Any

from orders.domain.entity.order import OrderEntity


class OrderSerializer(json.JSONEncoder):
    def default(self, o: OrderEntity) -> Any:
        try:
            to_serialize = {
                "order_id": str(o.order_id),
                "user_id": str(o.user_id),
                "value": str(o.value)
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
