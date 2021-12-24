import datetime
import json
from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest
from falcon import testing

from app import create_app
from payments.domain import Payment, PaymentStatus
from payments.repositories.payment_gateway import PaymentGatewayFactory
from payments.repositories.payment_info import PaymentInfoFactory
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


@mock.patch('payments.rest.PaymentInfoFactory')
def test_list(mocked_repository, client):
    repository = PaymentInfoFactory.make(implementation='IN_MEMORY',
                                         implementation_options=(payment_info_1, payment_info_2))
    mocked_repository.make.return_value = repository

    response = client.simulate_get('/payments')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(payments, cls=PaymentSerializer))


@mock.patch('payments.rest.PaymentInfoFactory')
def test_get_payment_by_id_when_payment_exists(mocked_payment_gateway_factory, client):
    repository = PaymentInfoFactory.make(implementation='IN_MEMORY',
                                         implementation_options=(payment_info_1, payment_info_2))
    mocked_payment_gateway_factory.make.return_value = repository

    response = client.simulate_get(f'/payments/{str(payments[0].payment_id)}')

    assert response.status_code == 200
    assert response.json == json.loads(json.dumps(payments[0], cls=PaymentSerializer))


@mock.patch('payments.rest.PaymentInfoFactory')
@mock.patch('payments.rest.PaymentGatewayFactory')
def test_payment_charge_user_by_payment_info(mocked_payment_gateway_factory, mocked_payment_info_factory, client):
    payment_gateway_repo = PaymentGatewayFactory.make(implementation='IN_MEMORY',
                                                      implementation_options=(payment_info_1, payment_info_2))
    mocked_payment_gateway_factory.make.return_value = payment_gateway_repo
    payment_info_repo = PaymentInfoFactory.make(implementation='IN_MEMORY',
                                                implementation_options=(payment_info_1, payment_info_2))
    mocked_payment_info_factory.make.return_value = payment_info_repo

    response = client.simulate_post(f'/payments/{str(payments[0].payment_id)}/charge')

    assert response.status_code == 200
    assert response.json == {"status": PaymentStatus.OK.name}
