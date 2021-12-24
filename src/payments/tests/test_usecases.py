from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest

from payments.domain import Payment, PaymentStatus
from payments.usecases import payments_list_usecase, payments_get_by_payment_id_usecase


@pytest.fixture
def available_payments():
    payment_user_1 = Payment(
        payment_id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        value=Decimal(999.59),
        status=PaymentStatus.OK
    )

    payment_user_2 = Payment(
        payment_id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        value=Decimal(345.59),
        status=PaymentStatus.OK
    )

    payment_user_3 = Payment(
        payment_id=uuid4(),
        user_id=uuid4(),
        order_id=uuid4(),
        value=Decimal(10877.59),
        status=PaymentStatus.FAILED_ON_GATEWAY
    )

    return [payment_user_1, payment_user_2, payment_user_3]


def test_payment_list_without_parameters(available_payments):
    repo = mock.Mock()
    repo.list.return_value = available_payments

    result = payments_list_usecase(repo)

    assert result == available_payments


def test_payments_get_by_payment_id_when_is_available(available_payments):
    payment = available_payments[0]
    repo = mock.Mock()
    repo.get_by_payment_id.return_value = payment

    result = payments_get_by_payment_id_usecase(repo, payment_id=payment.payment_id)

    assert result == payment
