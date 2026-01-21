from django import forms
from .models import Expense, ExpenseCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'ex_name', 'date', 'amount', 'note']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'ex_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ব্যয়ের নাম'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'পরিমাণ'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'নোট '}),
        }

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'নতুন ক্যাটেগরি'}),
        }
