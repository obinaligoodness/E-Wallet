import uuid
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Wallet, Transaction
from .seriallizers import WalletSerializer, TransactionActivitySerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionActivitySerializer
    @transaction.atomic()
    def create(self,request,*args,**kwargs):
        user = self.request.user
        wallet = get_object_or_404(Wallet, user=user.id)
        balance = wallet.balance
        transaction_details = {}
        serializer = TransactionActivitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.data['transaction_type'] == 'CREDIT':
                balance = wallet.balance + Decimal(serializer.data['amount'])
            elif serializer.data['transaction_type'] == 'DEBIT':
                if Decimal(serializer.data['amount']) < wallet.balance:
                    balance = wallet.balance - Decimal(serializer.data['amount'])
                else:
                    return Response(data="Insufficient funds",status=status.HTTP_400_BAD_REQUEST)

            elif serializer.data['transaction_type'] == 'TRANSFER':
                if Decimal(serializer.data['amount']) < wallet.balance:
                    balance = wallet.balance - Decimal(serializer.data['amount'])
                else:
                    return Response(data="Insufficient funds", status=status.HTTP_400_BAD_REQUEST)

                try:
                    wallet_to_transfer_to = Wallet.objects.get(
                        wallet_number=serializer.data['wallet_number'])
                except Wallet.DoesNotExist:
                    return Response(data={"message":"Account with the wallet number not found "}, status=status.HTTP_400_BAD_REQUEST)
                transferred_balance = wallet_to_transfer_to +  Decimal(serializer.data['amount'])
                Wallet.objects.filter(user_id= wallet_to_transfer_to.user_id).update(balance=transferred_balance)

            else:
                return Response(data="Invalid transaction",status=status.HTTP_400_BAD_REQUEST)
            Wallet.objects.filter(user_id=user.id).update(balance=balance)
            transaction_details['New Balance'] = balance
            transaction_details['Transaction type'] = serializer.data['transaction_type']
            transaction_details['Name'] = f"{wallet.user.last_name} {wallet.user.first_name}"
            transaction_details['Time'] = wallet.time_created
            transaction_details['Amount'] = serializer.data['amount']
            transaction_details['Description'] = serializer.data.get('description',"Transaction Description Not Provided")

            transactions = Transaction()
            transactions.wallet = wallet
            transactions.amount = serializer.data['amount']
            transactions.type = serializer.data['transaction_type']
            transactions.description = serializer.data.get('description',"Transaction Description Not provided")
            transactions.save()

            return Response(data=transaction_details,status=status.HTTP_200_OK)

        def retrieve(self, request, *args, **kwargs):
            return Response(data=transaction_details,status=status.HTTP_405_METHOD_NOT_ALLOWED)

        def list(self, request):
            return Response(data="Method not supported", status=status.HTTP_405_METHOD_NOT_ALLOWED)

class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
