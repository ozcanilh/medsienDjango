# medbank_api/tests/factories.py
import factory
from medbank_api.models import Customer, Account, Transfer


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker('name')
    email = factory.Faker('email')


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    customer = factory.SubFactory(CustomerFactory)
    balance = factory.Faker('pydecimal', left_digits=5, right_digits=2)


class TransferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transfer

    sender = factory.SubFactory(AccountFactory)
    receiver = factory.SubFactory(AccountFactory)
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2)
