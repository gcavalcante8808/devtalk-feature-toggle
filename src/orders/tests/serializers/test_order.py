import json
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from orders.domain.entity.order import OrderEntity, OrderStatus
from orders.domain.serializers.order import OrderSerializer


def test_serialize_order():
    user_id = uuid4()
    order_id = uuid4()
    value = Decimal(399.50)
    init_dict = {
        "user_id": user_id,
        "order_id": order_id,
        "value": value,
        "status": OrderStatus.OPEN
    }
    order = OrderEntity.from_dict(init_dict)

    json_order = json.dumps(order, cls=OrderSerializer)
    expected_json = json.dumps(SimpleNamespace(**init_dict), cls=OrderSerializer)

    assert json.loads(json_order) == json.loads(expected_json)
