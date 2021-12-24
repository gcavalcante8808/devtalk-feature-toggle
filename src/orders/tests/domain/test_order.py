from decimal import Decimal
from uuid import uuid4

from orders.domain.entity.order import OrderEntity, OrderStatus


def test_order_from_dict():
    user_id = uuid4()
    order_id = uuid4()
    init_dict = {
        "user_id": user_id,
        "order_id": order_id,
        "value": Decimal(399.50),
        "status": OrderStatus.OPEN
    }

    order = OrderEntity.from_dict(init_dict)

    assert order.order_id == order_id
    assert order.user_id == user_id
    assert order.value == Decimal(399.50)
    assert order.status == OrderStatus.OPEN


def test_order_to_dict():
    user_id = uuid4()
    order_id = uuid4()
    init_dict = {
        "user_id": user_id,
        "order_id": order_id,
        "value": Decimal(399.50),
        "status": OrderStatus.OPEN
    }

    order = OrderEntity.from_dict(init_dict)

    assert order.to_dict() == init_dict
