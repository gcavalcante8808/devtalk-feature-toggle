import enum

from payments.domain import PaymentStatus


class InMemoryPaymentGateway:
    def __init__(self, data=None):
        self.data = data if data else set()

    def charge_customer_using_payment_info(self, payment):
        payment = [entry for entry in self.data if payment.payment_id == entry['payment_id']]
        if payment:
            return PaymentStatus.OK

        return PaymentStatus.ORDER_NOT_FOUND


class PaymentGatewayImplementations(enum.Enum):
    IN_MEMORY = InMemoryPaymentGateway


class PaymentGatewayFactory:
    @staticmethod
    def make(implementation='IN_MEMORY', implementation_options=None):
        klass = getattr(PaymentGatewayImplementations, implementation)
        return klass.value(implementation_options)
