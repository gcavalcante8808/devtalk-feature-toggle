from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest

from payments.domain.entities import Payment, PaymentStatus
from payments.domain.usecases import payments_list_usecase


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
