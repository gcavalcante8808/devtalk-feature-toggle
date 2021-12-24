import datetime
import enum
import uuid
from dataclasses import dataclass, field, asdict
from decimal import Decimal


class PaymentStatus(enum.IntEnum):
    OK = 0
    FAILED_ON_GATEWAY = 1
    PENDING_ON_GATEWAY = 2
    COMMUNICATION_ERROR = 3


@dataclass
class Payment:
    payment_id: uuid.UUID
    order_id: uuid.UUID
    user_id: uuid.UUID
    value: Decimal
    status: PaymentStatus
    timestamp: int = datetime.datetime.now().timestamp()
    raw_response: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)
