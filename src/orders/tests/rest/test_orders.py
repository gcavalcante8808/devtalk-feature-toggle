import json
from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest
from falcon import testing

from app import create_app
from orders.domain.entity.order import OrderEntity, OrderStatus
from orders.domain.serializers.order import OrderSerializer

order = {
    "user_id": uuid4(),
    "order_id": uuid4(),
    "value": Decimal(309.80),
    "status": OrderStatus.OPEN
}
orders = [OrderEntity.from_dict(order)]


@pytest.fixture
def client():
    return testing.TestClient(create_app())


@mock.patch('orders.rest.orders.OrderGatewayInMemory')
def test_list(mocked_usecase, client):
    mocked_usecase().list.return_value = orders

    response = client.simulate_get('/orders')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(orders, cls=OrderSerializer))


@mock.patch('orders.rest.orders.OrderGatewayInMemory')
def test_get_order_by_id_when_order_exists(mocked_usecase, client):
    mocked_usecase().get_by_id.return_value = orders[0]

    response = client.simulate_get(f'/orders/{str(orders[0].order_id)}')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(orders[0], cls=OrderSerializer))


@mock.patch('orders.rest.orders.OrderGatewayInMemory')
def test_set_payment_status_by_order_id_when_orders_exists_and_status_is_correct(mocked_usecase, client):
    order = orders[0]
    order.status = OrderStatus.PENDING
    mocked_usecase().orders_set_payment_status_by_order_id.return_value = order

    response = client.simulate_put(f'/orders/{str(orders[0].order_id)}/status',
                                   json={'status': OrderStatus.PENDING.name})

    assert response.status_code == 204
