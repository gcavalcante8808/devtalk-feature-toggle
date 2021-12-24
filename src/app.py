import falcon
from werkzeug.serving import run_simple

from orders.rest.orders import OrderResource


def create_app():
    app = falcon.App()
    app.add_route('/orders', OrderResource())
    app.add_route('/orders/{order_id:uuid()}', OrderResource())
    app.add_route('/orders/{order_id:uuid()}/status', OrderResource())

    return app


if __name__ == '__main__':
    app = create_app()
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
