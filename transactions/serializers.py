from rest_framework import serializers
from transactions.models import Transaction
from customers.models import Customer

class TransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=Customer.objects.all())
    class Meta:
        model = Transaction
        fields = ['reference', 'account', 'date', 'amount', 'type', 'category', 'user_id']