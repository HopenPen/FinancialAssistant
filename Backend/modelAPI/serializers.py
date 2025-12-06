from rest_framework.serializers import ModelSerializer
from .models import Transaction

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    # Проверка: дата должна быть позже самой позднейшей даты в базе
    def create(self, validated_data):
        latest_transaction = Transaction.objects.order_by('-date').first()
        new_balance = latest_transaction.Balance if latest_transaction else 0
        if 'Deposit' in validated_data:
            new_balance += validated_data['Deposit']
        if 'Withdrawal' in validated_data:
            new_balance -= validated_data['Withdrawal']
        if latest_transaction and validated_data['date'] <= latest_transaction.date:
            raise ValueError("The date must be later than the latest transaction date in the database.")
        validated_data['Balance'] = new_balance
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    # Проверка: при обновлении транзакции дата не должна изменяться
    def update(self, instance, validated_data):
        latest_transaction = Transaction.objects.order_by('-date').first()
        new_balance = latest_transaction.Balance if latest_transaction else 0
        if 'Deposit' in validated_data:
            new_balance += validated_data['Deposit']
        if 'Withdrawal' in validated_data:
            new_balance -= validated_data['Withdrawal']
        if 'date' in validated_data and validated_data['date'] != instance.date:
            raise ValueError("The date of the transaction cannot be changed.")
        validated_data['Balance'] = new_balance
        return super().update(instance, validated_data)
    
class IncompleteTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['Withdrawal', 'Deposit', 'Balance']