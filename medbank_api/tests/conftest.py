from pytest_factoryboy import register

from medbank_api.tests.factories import AccountFactory, CustomerFactory, TransferFactory

register(AccountFactory)
register(CustomerFactory)
register(TransferFactory)
