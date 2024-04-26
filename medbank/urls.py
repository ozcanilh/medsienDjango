# banking_project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from medbank_api.views import CustomerViewSet, AccountViewSet, TransferViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transfers', TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]