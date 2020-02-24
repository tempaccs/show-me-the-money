from rest_framework import viewsets, permissions, mixins
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

class TransactionViewSet(
    mixins.CreateModelMixin, 
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


