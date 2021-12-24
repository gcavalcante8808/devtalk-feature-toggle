import datetime
import json
from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest
from falcon import testing

from app import create_app
from payments.domain import Payment, PaymentStatus
from payments.repository import PaymentInMemory
from payments.serializers import PaymentSerializer


payment_info = {
    "payment_id": uuid4(),
    "user_id": uuid4(),
    "order_id": uuid4(),
    "status": PaymentStatus.OK,
    "timestamp": datetime.datetime.now().timestamp(),
    "value": Decimal(576.99),
    "raw_response": {}
}
payments = [Payment.from_dict(payment_info)]


@pytest.fixture
def client():
    return testing.TestClient(create_app())


@mock.patch('payments.rest.PaymentInMemory')
def test_list(mocked_usecase, client):
    mocked_usecase().list.return_value = payments

    response = client.simulate_get('/payments')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(payments, cls=PaymentSerializer))


@mock.patch('payments.rest.PaymentInMemory')
def test_get_payment_by_id_when_payment_exists(mocked_usecase, client):
    mocked_usecase().get_payment_by_id.return_value = payments[0]

    response = client.simulate_get(f'/payments/{str(payments[0].payment_id)}')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(payments[0], cls=PaymentSerializer))
