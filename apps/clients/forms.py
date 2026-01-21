from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'



from .models import CustomerSupport

class CustomerSupportForm(forms.ModelForm):
    class Meta:
        model = CustomerSupport
        fields = ['message']  # Customer only submits a message
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'আপনার প্রশ্ন লিখুন...',
                'rows': 4,
            }),
        }



# class CustomerSupportAdminForm(forms.ModelForm):
#     class Meta:
#         model = CustomerSupport
#         fields = ['message', 'reply', 'status']
#         widgets = {
#             'message': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 4,
#                 'placeholder': 'কাস্টমারের মেসেজ',
#                 'readonly': True  # Optional: make it read-only
#             }),
#             'reply': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3,
#                 'placeholder': 'অ্যাডমিনের উত্তর লিখুন...'
#             }),
#             'status': forms.Select(attrs={'class': 'form-select'}),
#         }


# from django import forms
# from .models import CustomerSupport
class CustomerSupportAdminForm(forms.ModelForm):
    class Meta:
        model = CustomerSupport
        fields = ['message', 'status']  # reply বাদ দেওয়া হয়েছে
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'readonly': True,  # এটা read-only করে দিলাম
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
