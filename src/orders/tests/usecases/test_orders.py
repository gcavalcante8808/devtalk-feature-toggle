from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest

from orders.domain.entity.order import OrderEntity, OrderStatus
from orders.domain.usecases.order import orders_list_usecase, orders_get_by_id_usecase, \
    orders_set_payment_status_by_order_id


@pytest.fixture
def available_orders():
    order_1 = OrderEntity(
        user_id=uuid4(),
        order_id=uuid4(),
        value=Decimal(999.59),
        status=OrderStatus.OPEN
    )

    order_2 = OrderEntity(
        user_id=uuid4(),
        order_id=uuid4(),
        value=Decimal(76.59),
        status=OrderStatus.OPEN
    )

    order_3 = OrderEntity(
        user_id=uuid4(),
        order_id=uuid4(),
        value=Decimal(188.59),
        status=OrderStatus.OPEN
    )

    return [order_1, order_2, order_3]


def test_orders_list_without_parameters(available_orders):
    repo = mock.Mock()
    repo.list.return_value = available_orders

    result = orders_list_usecase(repo)

    assert result == available_orders


def test_orders_get_by_id_when_id_is_available(available_orders):
    repo = mock.Mock()
    repo.get_by_id.return_value = available_orders[0]

    result = orders_get_by_id_usecase(repo, order_id=available_orders[0].order_id)

    assert result == available_orders[0]


def test_order_set_payment_status_to_pending(available_orders):
    repo = mock.Mock()
    order = available_orders[0]
    order.status = OrderStatus.PENDING
    repo.set_payment_status_by_order_id.return_value = order

    result = orders_set_payment_status_by_order_id(repo, status=OrderStatus.PENDING, order_id=order.order_id)

    assert result == order
