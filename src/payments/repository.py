from payments.domain import Payment, PaymentStatus


class PaymentInMemory:
    def __init__(self, data=None):
        self.data = data if data else set()

    def get_payment_by_id(self, payment_id) -> Payment:
        payment = [entry for entry in self.data if payment_id == entry['payment_id']]
        return Payment.from_dict(payment[0])

    def list(self) -> list[Payment]:
        return [Payment.from_dict(i) for i in self.data]


class InMemoryPaymentGatewayIntegration:
    def __init__(self, data=None):
        self.data = data if data else set()

    def charge_user_by_order_id(self, order_id):
        payment = [entry for entry in self.data if order_id == entry['order_id']]
        if payment:
            return PaymentStatus.OK

        return PaymentStatus.ORDER_NOT_FOUND
