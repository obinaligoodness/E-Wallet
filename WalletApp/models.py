import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from UserApp.models import User


# Create your models here.

class Wallet(models.Model):
    balance = models.DecimalField(max_digits= 9,decimal_places=2, default=0.00)
    user = models.OneToOneField(User, on_delete=models.PROTECT,)
    wallet_number = models.CharField(max_length=10, primary_key=True)
    time_created = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    status = [
        ('SUCCESSFUL', 'Successful'),
        ('PENDING', 'Pending'),
        ('DECLINED', 'Declined'),
    ]
    type = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
        ('WITHDRAW', 'Withdraw'),
    ]
    date_time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    ref_num = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
