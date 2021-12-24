import enum

from payments.domain import Payment


class InMemoryPaymentInfo:
    def __init__(self, data=None):
        self.data = data if data else set()

    def get_payment_by_id(self, payment_id) -> Payment:
        payment = [entry for entry in self.data if payment_id == entry['payment_id']]
        return Payment.from_dict(payment[0])

    def list(self) -> list[Payment]:
        return [Payment.from_dict(i) for i in self.data]


class PaymentInfoImplementations(enum.Enum):
    IN_MEMORY = InMemoryPaymentInfo


class PaymentInfoFactory:
    @staticmethod
    def make(implementation='IN_MEMORY', implementation_options=None):
        klass = getattr(PaymentInfoImplementations, implementation)
        return klass.value(implementation_options)
