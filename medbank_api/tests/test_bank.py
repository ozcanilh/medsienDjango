from django.urls import reverse
from rest_framework import status
import pytest

@pytest.mark.django_db
def test_create_customer(client):
    data = {'name': 'Test Customer', 'email': 'test@example.com'}
    response = client.post(path="/customers/", data=data)
    assert response.json()['name'] == 'Test Customer'
    assert response.json()['email'] == 'test@example.com'
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_customer_with_invalid_email(client):
    data = {'name': 'Test Customer', 'email': 'invalidemail'}
    response = client.post(path="/customers/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.json()


@pytest.mark.django_db
def test_create_account(client, account):
    data = {'customer': account.customer.id, 'balance': '1000.00'}
    response = client.post(path='/accounts/', data=data)
    assert response.json()['customer'] == account.customer.id
    assert response.json()['balance'] == '1000.00'
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_account_with_nonexistent_customer(client):
    data = {'customer': 9999, 'balance': '1000.00'}
    response = client.post(path='/accounts/', data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'customer' in response.json()

@pytest.mark.django_db
def test_create_account_with_negative_balance(client, customer_factory):
    customer = customer_factory()
    data = {'customer': customer.id, 'balance': '-100.00'}
    response = client.post(path='/accounts/', data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'balance' in response.json()

@pytest.mark.django_db
def test_create_transfer(client, account_factory):
    sender = account_factory(balance=1000)
    receiver = account_factory(balance=0)
    data = {'sender': sender.id, 'receiver': receiver.id, 'amount': 500}
    response = client.post(path='/transfers/', data=data)
    assert response.json()['sender'] == sender.customer.id
    assert response.json()['receiver'] == receiver.customer.id
    assert response.json()['amount'] == '500.00'
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_successful_money_transfer(client, account_factory, transfer_factory):
    sender = account_factory(balance=1000)
    receiver = account_factory(balance=0)

    data = {
        'sender': sender.id,
        'receiver': receiver.id,
        'amount': 500
    }

    response = client.post(path='/transfers/money/', data=data)

    assert response.json()['sender'] == sender.id
    assert response.json()['receiver'] == receiver.id
    assert response.status_code == status.HTTP_201_CREATED

    sender.refresh_from_db()
    receiver.refresh_from_db()

    assert sender.balance == 500
    assert receiver.balance == 500

@pytest.mark.django_db
def test_negative_or_zero_amount(client, account_factory):
    sender = account_factory(balance=1000)
    receiver = account_factory(balance=500)

    data = {'sender': sender.id, 'receiver': receiver.id, 'amount': 0}
    response = client.post(path='/transfers/money/', data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Amount should be positive" in response.json()['error']

    data['amount'] = -100
    response = client.post(path='/transfers/money/', data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Amount should be positive" in response.json()['error']

@pytest.mark.django_db
def test_account_not_found(client, account_factory):
    valid_account = account_factory(balance=1000)

    data = {'sender': 99999, 'receiver': valid_account.id, 'amount': 100}
    response = client.post(path='/transfers/money/', data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "One of the accounts does not exist" in response.json()['error']

    data = {'sender': valid_account.id, 'receiver': 99999, 'amount': 100}
    response = client.post(path='/transfers/money/', data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "One of the accounts does not exist" in response.json()['error']

@pytest.mark.django_db
def test_insufficient_funds(client, account_factory):
    sender = account_factory(balance=100)  # Bakiye transfer miktarından düşük
    receiver = account_factory(balance=500)
    data = {'sender': sender.id, 'receiver': receiver.id, 'amount': 500}
    response = client.post(path='/transfers/money/', data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Insufficient funds" in response.json()['error']

