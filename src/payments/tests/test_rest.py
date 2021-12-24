import datetime
import json
from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest
from falcon import testing

from app import create_app
from payments.domain import Payment, PaymentStatus
from payments.repositories.payment_info import InMemoryPaymentInfo
from payments.serializers import PaymentSerializer


payment_info_1 = {
    "payment_id": uuid4(),
    "user_id": uuid4(),
    "order_id": uuid4(),
    "status": PaymentStatus.OK,
    "timestamp": datetime.datetime.now().timestamp(),
    "value": Decimal(576.99),
    "raw_response": {}
}

payment_info_2 = {
    "payment_id": uuid4(),
    "user_id": uuid4(),
    "order_id": uuid4(),
    "status": PaymentStatus.WAITING_FOR_PAYMENT,
    "timestamp": datetime.datetime.now().timestamp(),
    "value": Decimal(999.99),
    "raw_response": {}
}

payments = [Payment.from_dict(payment_info_1), Payment.from_dict(payment_info_2)]


@pytest.fixture
def client():
    return testing.TestClient(create_app())


@mock.patch('payments.rest.InMemoryPaymentInfo')
def test_list(mocked_usecase, client):
    mocked_usecase().list.return_value = payments

    response = client.simulate_get('/payments')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(payments, cls=PaymentSerializer))


@mock.patch('payments.rest.InMemoryPaymentInfo')
def test_get_payment_by_id_when_payment_exists(mocked_usecase, client):
    mocked_usecase().get_payment_by_id.return_value = payments[0]

    response = client.simulate_get(f'/payments/{str(payments[0].payment_id)}')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(payments[0], cls=PaymentSerializer))


@mock.patch('payments.rest.InMemoryPaymentInfo')
@mock.patch('payments.rest.InMemoryPaymentGateway')
def test_payment_charge_user_by_payment_info(mocked_gateway_repo, mocked_payment_repo, client):
    mocked_payment_repo().get_payment_by_id.return_value = payments[0]
    mocked_gateway_repo().charge_customer_using_payment_info.return_value = PaymentStatus.OK

    response = client.simulate_post(f'/payments/{str(payments[0].payment_id)}/charge')

    assert response.status_code == 200
    assert response.json == {"status": PaymentStatus.OK.name}
