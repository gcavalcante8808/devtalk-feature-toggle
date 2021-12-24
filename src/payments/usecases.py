from payments.domain import Payment


def payments_list_usecase(repository):
    return repository.list()


def payments_get_by_payment_id_usecase(repository, payment_id):
    return repository.get_payment_by_id(payment_id)


def payments_charge_customer_using_payment_info_usecase(repository, payment_info: Payment):
    return repository.charge_customer_using_payment_info(payment_info)
