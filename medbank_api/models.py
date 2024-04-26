# banking_app/models.py
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer}'s Account"


class Transfer(models.Model):
    sender = models.ForeignKey(Account, related_name='transfers_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='transfers_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.customer}'s Transfer to {self.receiver.customer} - {self.amount}"
