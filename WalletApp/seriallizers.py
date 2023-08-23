from rest_framework import serializers

from WalletApp.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'user', 'wallet_number']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['status', 'type', 'date_time', 'amount', 'wallet', 'ref_num']

