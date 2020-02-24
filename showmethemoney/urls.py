from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from transactions.views import TransactionViewSet
from customers.views import CustomerViewSet

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]