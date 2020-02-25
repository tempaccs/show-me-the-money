from rest_framework import viewsets, permissions, status, mixins
from customers.models import Customer
from customers.serializers import (
    CustomerSerializer,
    BalanceSerializer,
    CategorySerializer,
)
from transactions.models import Transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from_query_parameter = openapi.Parameter(
    "from",
    openapi.IN_QUERY,
    description="starting date for balance calculation",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)
to_query_parameter = openapi.Parameter(
    "to",
    openapi.IN_QUERY,
    description="ending date for balance calculation",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: BalanceSerializer(many=True)},
        manual_parameters=[from_query_parameter, to_query_parameter],
    )
    @action(detail=True)
    def balance(self, request, pk):
        queryset = Transaction.objects.filter(user=pk)
        from_date = self.request.query_params.get("from", None)
        to_date = self.request.query_params.get("to", None)

        if from_date:
            queryset = queryset.filter(date__gte=from_date)

        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        data = queryset.values("account").annotate(
            balance=Sum("amount"),
            total_inflow=Coalesce(Sum("amount", filter=Q(type="inflow")), 0),
            total_outflow=Coalesce(Sum("amount", filter=Q(type="outflow")), 0),
        )
        return Response(
            BalanceSerializer(data, many=True).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: CategorySerializer()})
    @action(detail=True)
    def categories(self, request, pk):
        # Getting all the transactions grouped by category, and isolated cateogry and sum...
        queryset = (
            Transaction.objects.filter(user=pk)
            .values("category")
            .annotate(sum=Sum("amount"))
            .values_list("category", "sum")
        )

        # ...and then filter them by type
        data = {
            "inflow": dict(queryset.filter(type="inflow")),
            "outflow": dict(queryset.filter(type="outflow")),
        }
        return Response(CategorySerializer(data).data, status=status.HTTP_200_OK)
