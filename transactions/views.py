from rest_framework import viewsets, permissions
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


