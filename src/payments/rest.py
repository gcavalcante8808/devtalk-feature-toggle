import json

import falcon

from payments.repository import PaymentInMemory, InMemoryPaymentGatewayIntegration
from payments.serializers import PaymentSerializer
from payments.usecases import payments_list_usecase, payments_get_by_payment_id_usecase, \
    payments_charge_customer_using_payment_info_usecase


class PaymentResource:
    def on_get(self, req, resp, payment_id=None):

        if not payment_id:
            result = payments_list_usecase(PaymentInMemory())
        else:
            result = payments_get_by_payment_id_usecase(PaymentInMemory(), payment_id)

        resp.text = json.dumps(result, cls=PaymentSerializer)
        resp.status = falcon.HTTP_200


class ChargePaymentResource:
    def on_post(self, req, resp, payment_id):
        payment_info = payments_get_by_payment_id_usecase(PaymentInMemory(), payment_id)
        charge_result = payments_charge_customer_using_payment_info_usecase(InMemoryPaymentGatewayIntegration(), payment_info)

        resp.text = json.dumps({"status": charge_result.name})
        resp.status_code = falcon.HTTP_200
