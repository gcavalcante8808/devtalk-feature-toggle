import enum
import uuid
from dataclasses import dataclass, asdict
from decimal import Decimal


class OrderStatus(enum.IntEnum):
    OPEN = 1
    PENDING = 2


@dataclass
class OrderEntity:
    order_id: uuid.UUID
    user_id: uuid.UUID
    value: Decimal
    status: OrderStatus

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)
