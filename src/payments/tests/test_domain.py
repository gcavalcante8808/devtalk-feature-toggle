import datetime
from decimal import Decimal
from uuid import uuid4

from payments.domain import PaymentStatus, Payment


def test_payment_from_dict():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    timestamp = datetime.datetime.now().timestamp()
    status = PaymentStatus.OK

    init_dict = {
        "payment_id": payment_id,
        "user_id": user_id,
        "order_id": order_id,
        "status": status,
        "timestamp": timestamp,
        "value": Decimal(576.99),
        "raw_response": {}
    }

    payment = Payment.from_dict(init_dict)

    assert payment.order_id == order_id
    assert payment.user_id == user_id
    assert payment.value == Decimal(576.99)
    assert payment.payment_id == payment_id


def test_payment_to_dict():
    payment_id = uuid4()
    order_id = uuid4()
    user_id = uuid4()
    timestamp = datetime.datetime.now().timestamp()
    status = PaymentStatus.OK

    init_dict = {
        "payment_id": payment_id,
        "user_id": user_id,
        "order_id": order_id,
        "status": status,
        "timestamp": timestamp,
        "value": Decimal(576.99),
        "raw_response": {}
    }

    payment = Payment.from_dict(init_dict)

    assert payment.to_dict() == init_dict
