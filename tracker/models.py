from django.db import models

# Create your models here.


class currentbalance(models.Model):
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)


    def __str__(self):
        return f"Current Balance: ${self.balance} "


class Expense(models.Model):
    current_balance = models.ForeignKey(currentbalance, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=10, default='expense')

    def __str__(self):
        return f"{self.description} - ${self.amount} on {self.date} ({self.type})"
