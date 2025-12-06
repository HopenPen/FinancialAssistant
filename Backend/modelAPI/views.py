from .models import Transaction
from .serializers import TransactionSerializer
from .MLModels.predictions import make_prediction, make_dataframe
from rest_framework import views, viewsets, permissions
from rest_framework.response import Response

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all().order_by('date')
    serializer_class = TransactionSerializer

class CategoryPredictionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        input_data = make_dataframe(
            withdrawal=request.data.get('Withdrawal', 0),
            deposit=request.data.get('Deposit', 0),
            balance=request.data.get('Balance', 0)
        )
        prediction = make_prediction(input_data)
        return Response({'predicted_category': prediction})
