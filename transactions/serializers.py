from rest_framework import serializers
from transactions.models import Transaction, Flow
from customers.models import Customer


class TransactionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["type"] == Flow.INFLOW and data["amount"] < 0:
            raise serializers.ValidationError("inflow amount must be > 0.")
        if data["type"] == Flow.OUTFLOW and data["amount"] > 0:
            raise serializers.ValidationError("outflow amount must be < 0.")
        return data

    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=Customer.objects.all()
    )

    class Meta:
        model = Transaction
        fields = [
            "reference",
            "account",
            "date",
            "amount",
            "type",
            "category",
            "user_id",
        ]
