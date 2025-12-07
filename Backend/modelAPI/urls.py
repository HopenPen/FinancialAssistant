from django.urls import path, include
from rest_framework import routers
from .views import TransactionView, CategoryPredictionView, PrognoseView

urlpatterns = [
    path('transactions/', TransactionView.as_view(), name='transaction-list'),
    path('predict-category/', CategoryPredictionView.as_view(), name='predict-category'),
    path('prognose/', PrognoseView.as_view(), name='prognose'),
]