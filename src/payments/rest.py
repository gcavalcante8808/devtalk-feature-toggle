import json

import falcon

from payments.repository import PaymentInMemory
from payments.serializers import PaymentSerializer
from payments.usecases import payments_list_usecase, payments_get_by_payment_id_usecase


class PaymentResource:
    def on_get(self, req, resp, payment_id=None):

        if not payment_id:
            result = payments_list_usecase(PaymentInMemory())
        else:
            result = payments_get_by_payment_id_usecase(PaymentInMemory(), payment_id)

        resp.text = json.dumps(result, cls=PaymentSerializer)
        resp.status = falcon.HTTP_200
