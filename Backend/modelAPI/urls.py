from django.urls import path, include
from rest_framework import routers
from .views import TransactionViewSet, CategoryPredictionView

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict-category/', CategoryPredictionView.as_view(), name='predict-category'),
]