from decimal import Decimal
from uuid import uuid4

import pytest

from orders.domain.entity.order import OrderEntity, OrderStatus
from orders.domain.repository.order import OrderGatewayInMemory


@pytest.fixture
def available_orders():
    order_1 = {
        "user_id": uuid4(),
        "order_id": uuid4(),
        "value": Decimal(999.59),
        "status": OrderStatus.OPEN
    }

    order_2 = {
        "user_id": uuid4(),
        "order_id": uuid4(),
        "value": Decimal(76.59),
        "status": OrderStatus.OPEN
    }

    order_3 = {
        "user_id": uuid4(),
        "order_id": uuid4(),
        "value": Decimal(188.59),
        "status": OrderStatus.OPEN
    }

    return [order_1, order_2, order_3]


def test_repository_list_without_parameters(available_orders):
    repo = OrderGatewayInMemory(available_orders)

    orders = [OrderEntity.from_dict(order) for order in available_orders]

    assert repo.list() == orders


def test_repository_with_order_id(available_orders):
    repo = OrderGatewayInMemory(available_orders)
    order_id = available_orders[0]['order_id']

    order = repo.get_order_by_id(order_id)

    assert order == OrderEntity.from_dict(available_orders[0])
