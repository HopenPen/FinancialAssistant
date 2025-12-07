from .models import Transaction
from .serializers import TransactionCreateSerializer
from .MLModels.predictions import make_prediction, make_dataframe
from rest_framework import views, permissions
from rest_framework.response import Response
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models

class CategoryPredictionView(views.APIView):
    def post(self, request, *args, **kwargs):
        input_data = make_dataframe(
            withdrawal=request.data.get('Withdrawal', 0),
            deposit=request.data.get('Deposit', 0),
            balance=request.data.get('Balance', 0)
        )
        prediction = make_prediction(input_data)
        return Response({'predicted_category': prediction})
    
class TransactionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user).order_by('date')
        serializer = TransactionCreateSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TransactionCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class PrognoseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]        

    def get(self, request, *args, **kwargs):
        latest_date = Transaction.objects.filter(user=request.user).aggregate(models.Max('date'))['date__max']
        latest_transaction = Transaction.objects.filter(user=request.user).order_by('-date').first()

        if not latest_date:
            return None

        month_ago = latest_date - relativedelta(months=1)

        month_ago = Transaction.objects.filter(user=request.user, date__gte=month_ago, date__lte=latest_date).order_by('-date').first()
        if month_ago is None:
            prognosis = "Недостаточно данных для прогноза."
            balance_state = 0
        else:
            balance_difference = latest_transaction.Balance - month_ago.Balance
            if balance_difference >= 0:
                prognosis = "Ваш бюджет стабилен."
                balance_state = 1
            else:
                month_remaining = latest_transaction.Balance / abs(balance_difference)
                prognosis = f"Ваш бюджет закончится через {month_remaining:.1f} месяцев."
                balance_state = -1
        latest_transaction = Transaction.objects.filter(user=request.user).order_by('-date').first()
        if balance_state == 0:
            cushion = "Невозможно рассчитать финансовую подушку из-за недостатка данных."
        elif balance_state == 1 or latest_transaction.Balance + balance_difference * 6 >= 0:
            cushion = "Вам не требуется финансовая подушка."
        else:
            cushion = f"Рекомендуется создать минимальную финансовую подушку в размере {abs(latest_transaction.Balance + balance_difference * 6)} на 6 месяцев."
        print(prognosis)
        print(cushion)
        return Response({'message': prognosis + '\n' + cushion + '\n'})