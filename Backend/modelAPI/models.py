from django.db import models
from django.conf import settings

class Transaction(models.Model):
    class TransactionCategory(models.TextChoices):
        FOOD = 'FD', 'Food'
        TANSPORT = 'TR', 'Transport'
        RENT = 'RT', 'Rent'
        SALARY = 'SL', 'Salary'
        SHOPPING = 'SP', 'Shopping'
        MISC = 'MS', 'Miscellaneous'

    Category = models.CharField(max_length=2, choices=TransactionCategory.choices)
    date = models.DateField()
    
    RefNo = models.CharField(max_length=50)
    Withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Balance = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
