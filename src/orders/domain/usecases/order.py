def orders_list_usecase(order_gateway) -> object:
    return order_gateway.list()


def orders_get_by_id_usecase(order_gateway, order_id):
    return order_gateway.get_by_id(order_id)


def orders_set_payment_status_by_order_id(order_gateway, status, order_id):
    return order_gateway.set_payment_status_by_order_id(status, order_id)
