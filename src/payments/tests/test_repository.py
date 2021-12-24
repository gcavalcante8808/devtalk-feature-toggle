from decimal import Decimal
from uuid import uuid4

import pytest

from payments.domain import Payment, PaymentStatus
from payments.repository import PaymentInMemory, InMemoryPaymentGatewayIntegration


@pytest.fixture
def available_payments():
    payment_user_1 = {
        "payment_id": uuid4(),
        "user_id": uuid4(),
        "order_id": uuid4(),
        "value": Decimal(999.59),
        "status": PaymentStatus.OK
    }

    payment_user_2 = {
        "payment_id": uuid4(),
        "user_id": uuid4(),
        "order_id": uuid4(),
        "value": Decimal(345.59),
        "status": PaymentStatus.OK
    }

    payment_user_3 = {
        "payment_id": uuid4(),
        "user_id": uuid4(),
        "order_id": uuid4(),
        "value": Decimal(10877.59),
        "status": PaymentStatus.FAILED_ON_GATEWAY
    }

    return [payment_user_1, payment_user_2, payment_user_3]


def test_repository_list_without_parameters(available_payments):
    repo = PaymentInMemory(available_payments)

    payments = [Payment.from_dict(payment) for payment in available_payments]

    assert repo.list() == payments


def test_repository_list_by_payment_id(available_payments):
    repo = PaymentInMemory(available_payments)
    payment_id = available_payments[0]['payment_id']

    payment = repo.get_payment_by_id(payment_id)

    assert payment == Payment.from_dict(available_payments[0])


def test_repository_charge_user_by_order_id_when_it_exists(available_payments):
    repo = InMemoryPaymentGatewayIntegration(available_payments)
    payment_info = Payment.from_dict(available_payments[0])

    payment_result = repo.charge_customer_using_payment_info(payment_info)

    assert payment_result == PaymentStatus.OK


def test_repository_charge_fails_when_order_doesnt_exists_doesnt_exists(available_payments):
    repo = InMemoryPaymentGatewayIntegration()
    payment_info = Payment.from_dict(available_payments[0])

    payment_result = repo.charge_customer_using_payment_info(payment_info)

    assert payment_result == PaymentStatus.ORDER_NOT_FOUND
