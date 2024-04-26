# banking_app/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, Account, Transfer
from .serializers import CustomerSerializer, AccountSerializer, TransferSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    @action(detail=False, methods=['post'])
    def money(self, request):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        amount = int(request.data.get('amount'))

        if amount <= 0:
            return Response({'error': 'Amount should be positive'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = Account.objects.get(pk=sender_id)
            receiver = Account.objects.get(pk=receiver_id)
        except Account.DoesNotExist:
            return Response({'error': 'One of the accounts does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if sender.balance < amount:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        sender.balance -= amount
        receiver.balance += amount

        sender.save()
        receiver.save()

        transfer = Transfer.objects.create(sender=sender, receiver=receiver, amount=amount)

        serializer = TransferSerializer(transfer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)