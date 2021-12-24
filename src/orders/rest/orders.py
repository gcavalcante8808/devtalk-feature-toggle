import json

import falcon

from orders.domain.entity.order import OrderStatus
from orders.domain.repository.order import OrderGatewayInMemory
from orders.domain.serializers.order import OrderSerializer
from orders.domain.usecases.order import orders_list_usecase, orders_get_by_id_usecase, \
    orders_set_payment_status_by_order_id


class OrderResource:
    def on_get(self, req, resp, order_id=None):
        if not order_id:
            result = orders_list_usecase(OrderGatewayInMemory())
        else:
            result = orders_get_by_id_usecase(OrderGatewayInMemory(), order_id)

        resp.text = json.dumps(result, cls=OrderSerializer)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, order_id):
        expected_status = req.get_media().get('status')

        status = getattr(OrderStatus, expected_status)

        orders_set_payment_status_by_order_id(order_gateway=OrderGatewayInMemory(), status=status, order_id=order_id)

        resp.status = falcon.HTTP_204
