from rest_framework import viewsets, status, mixins
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response


class TransactionViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        request_body=TransactionSerializer(many=True),
        responses={status.HTTP_201_CREATED: TransactionSerializer(many=True)},
    )
    def create(self, request):
        serializer = TransactionSerializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        transactions = serializer.save()
        return Response(
            TransactionSerializer(transactions, many=True).data,
            status=status.HTTP_201_CREATED,
        )
