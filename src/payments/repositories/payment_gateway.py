from payments.domain import PaymentStatus


class InMemoryPaymentGateway:
    def __init__(self, data=None):
        self.data = data if data else set()

    def charge_customer_using_payment_info(self, payment):
        payment = [entry for entry in self.data if payment.payment_id == entry['payment_id']]
        if payment:
            return PaymentStatus.OK

        return PaymentStatus.ORDER_NOT_FOUND