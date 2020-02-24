from rest_framework import viewsets
from customers.models import Customer
from customers.serializers import CustomerSerializer
from rest_framework import permissions

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

