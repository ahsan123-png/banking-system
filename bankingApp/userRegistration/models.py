import random
import string
from django.db import models


class UserEx(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    accountType = models.CharField(max_length=100)
    email = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=15,)
    cnic = models.CharField(max_length=15, unique=True)
    bank_name = models.CharField(max_length=100,default="Default")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'bank'):
            bank_name=self.bank_name
            acc_no = self.generate_account_number()
            ibmn_no = self.generate_ibmn_number()
            bank = Bank.objects.create(user=self, bank_name=bank_name, acc_no=acc_no, ibmn_no=ibmn_no)
            Account.objects.create(user=self, acc_no=acc_no, ibmn_no=ibmn_no, balance=0.00)

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def generate_ibmn_number(self):
        return f'IB{self.cnic[:2]}{"".join(random.choices(string.digits + string.ascii_uppercase, k=16))}'

class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    acc_no = models.CharField(max_length=20, unique=True)
    ibmn_no = models.CharField(max_length=20, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(UserEx, on_delete=models.CASCADE, related_name='bank')

class Account(models.Model):
    acc_no = models.CharField(max_length=20, unique=True)
    ibmn_no = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE, related_name='accounts')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=70,blank=True,null=True)
    type = models.CharField(max_length=70,blank=True,null=True)
class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=70,blank=True,null=True)