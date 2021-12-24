import json
from typing import Any

from payments.domain import Payment


class PaymentSerializer(json.JSONEncoder):
    def default(self, o: Payment) -> Any:
        try:
            to_serialize = {
                "payment_id": str(o.payment_id),
                "order_id": str(o.order_id),
                "user_id": str(o.user_id),
                "value": str(o.value),
                "status": o.status,
                "timestamp": int(o.timestamp),
                "raw_response": o.raw_response
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
