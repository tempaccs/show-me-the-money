from rest_framework import viewsets, permissions, status, mixins
from customers.models import Customer
from customers.serializers import CustomerSerializer
from rest_framework import permissions
from transactions.models import Transaction
from rest_framework.decorators import action
from transactions.serializers import TransactionSerializer
from rest_framework.response import Response

class CustomerViewSet(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True)
    def transactions(self, request, pk):
        queryset = Transaction.objects.filter(user=pk)
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        
        if (from_date):
            queryset = queryset.filter(date__gte=from_date)

        if (to_date):
            queryset = queryset.filter(date__lte=to_date)
            
        return Response(TransactionSerializer(queryset, many=True).data, status=status.HTTP_200_OK)