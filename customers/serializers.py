from rest_framework import serializers
from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "age"]


class BalanceSerializer(serializers.Serializer):
    account = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_inflow = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=10, decimal_places=2)


class CategorySerializer(serializers.Serializer):
    inflow = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )
    outflow = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )
