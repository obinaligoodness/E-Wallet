import uuid
from datetime import datetime

from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Wallet, Transaction
from .seriallizers import WalletSerializer, TransactionSerializer


class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def transfer(self, sender_wallet_number, amount, receiver_wallet_number):
        sender = Wallet.objects.get(pk=sender_wallet_number)
        receiver = Wallet.objects.get(pk=receiver_wallet_number)

        transaction = Transaction.objects.create()
        transaction.type = 'TRANSFER'
        transaction.date_time = datetime.datetime.now()
        transaction.amount = amount
        transaction.wallet = sender
        transaction.reference_number = uuid.uuid4()

        if sender.balance > 0 and amount > 0:
            receiver.balance += amount
            sender.balance -= amount
            transaction.status = 'SUCCESSFUL'
            transaction.save()
            sender.save()

    def deposit(self, receiver_wallet_number, amount):
        receiver = Wallet.objects.get(pk=receiver_wallet_number)

        transaction = Transaction.objects.create()
        transaction.type = 'DEPOSIT'
        transaction.date_time = datetime.datetime.now()
        transaction.amount = amount
        transaction.wallet = receiver
        transaction.reference_number = uuid.uuid4()

        receiver.balance += amount
        transaction.save()
        receiver.save()


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
