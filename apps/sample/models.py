from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Expense Type", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses', verbose_name="Expense Category")
    ex_name = models.CharField(max_length=255, verbose_name="Expense Name", null=True, blank=True)
    date = models.DateField(verbose_name="Date")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    note = models.TextField(blank=True, null=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ex_name} - {self.amount} ৳"
