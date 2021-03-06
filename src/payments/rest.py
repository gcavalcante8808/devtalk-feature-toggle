import json

import falcon

from payments.repositories.payment_gateway import PaymentGatewayFactory
from payments.repositories.payment_info import PaymentInfoFactory
from payments.serializers import PaymentSerializer
from payments.usecases import payments_list_usecase, payments_get_by_payment_id_usecase, \
    payments_charge_customer_using_payment_info_usecase


class PaymentResource:
    def on_get(self, req, resp, payment_id=None):
        payment_repository = PaymentInfoFactory.make()

        if not payment_id:
            result = payments_list_usecase(payment_repository)
        else:
            result = payments_get_by_payment_id_usecase(payment_repository, payment_id)

        resp.text = json.dumps(result, cls=PaymentSerializer)
        resp.status = falcon.HTTP_200


class ChargePaymentResource:
    def on_post(self, req, resp, payment_id):
        payment_gateway_repo = PaymentGatewayFactory.make()
        payment_info_repo = PaymentInfoFactory.make()

        payment_info = payments_get_by_payment_id_usecase(payment_info_repo, payment_id)
        charge_result = payments_charge_customer_using_payment_info_usecase(payment_gateway_repo, payment_info)

        resp.text = json.dumps({"status": charge_result.name})
        resp.status_code = falcon.HTTP_200
