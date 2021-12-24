from orders.domain.entity.order import OrderEntity


class OrderGatewayInMemory:
    def __init__(self, data):
        self.data = data

    def get_order_by_id(self, order_id) -> OrderEntity:
        order = [entry for entry in self.data if order_id == entry['order_id']]
        return OrderEntity.from_dict(order[0])

    def list(self) -> list[OrderEntity]:
        return [OrderEntity.from_dict(i) for i in self.data]
