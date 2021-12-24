def payments_list_usecase(repository):
    return repository.list()


def payments_get_by_payment_id_usecase(repository, payment_id):
    return repository.get_payment_by_id(payment_id)
