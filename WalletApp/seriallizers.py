from rest_framework import serializers

from WalletApp.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'user', 'wallet_number']


class TransactionActivitySerializer(serializers.Serializer):
    transaction_type = [
        ('DEBIT', 'DEBIT'),
        ('CREDIT', 'CREDIT'),
        ('TRANSFER', 'TRANSFER')
    ]
    wallet_number = serializers.CharField(max_length=10,required=False)
    amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    transaction_type = serializers.ChoiceField(choices=transaction_type,default='DEBIT')
    description = serializers.CharField(max_length=200,required=False)

    def validate(self,data):
        if data.get('transaction_type') == 'TRANSFER' and data.get('wallet_number ') is None:
            raise serializers.ValidationError(
                "Wallet number must be provided for TRANSFER transaction type"
            )
        return super().validate(data)
