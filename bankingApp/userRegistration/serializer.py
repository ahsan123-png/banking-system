# serializers.py

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['sender',
                'receiver', 
                'amount', 
                'fee', 
                'timestamp', 
                'description', 
                'transaction_type']
