from rest_framework import viewsets
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework import permissions

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

