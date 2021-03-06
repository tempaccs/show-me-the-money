from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions
from transactions.views import TransactionViewSet
from customers.views import CustomerViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r"transactions", TransactionViewSet)
router.register(r"customers", CustomerViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Show-Me-The-Money API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
