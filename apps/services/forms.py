from django import forms
from django.utils import timezone
from .models import ClientServices, ServiceApplication, Notice,NoticePublic

class ClientServicesForm(forms.ModelForm):
    class Meta:
        model = ClientServices
        fields = ['name', 'description', 'image', 'price', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
# from django import forms
# from django.utils import timezone
# from .models import ServiceApplication

# class ServiceApplicationPaymentForm(forms.ModelForm):
#     class Meta:
#         model = ServiceApplication
#         fields = ['status', 'amount_paid', 'payment_message', 'discount', 'action_taken', 'payment_due_date']

#     # Read-only computed field for UI display
#     due_amount = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         required=False,
#         label="Due Amount",
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
#     )

#     ACTION_CHOICES = [
#         ('none', 'None'),
#         ('partial_payment', 'Partial Payment'),
#         ('full_payment', 'Full Payment'),
#     ]

#     action_taken = forms.ChoiceField(
#         choices=ACTION_CHOICES,
#         widget=forms.Select(attrs={'class': 'form-select'})
#     )

#     payment_due_date = forms.DateField(
#         widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#         initial=timezone.now().date(),
#         required=False
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # ✅ Mark amount_paid as not required so we can set it dynamically
#         self.fields['amount_paid'].required = False

#         # Set default values
#         if self.instance:
#             self.fields['amount_paid'].initial = self.instance.balance
#             self.fields['due_amount'].initial = self.instance.balance

#         # Disable discount field if already used
#         if self.instance.discount_used:
#             self.fields['discount'].widget.attrs['disabled'] = 'disabled'
#             self.fields['discount'].required = False

#     def clean_amount_paid(self):
#         """
#         If user doesn't enter a value, fall back to current balance.
#         """
#         amount_paid = self.cleaned_data.get('amount_paid')
#         if amount_paid in [None, '']:
#             return self.instance.balance
#         return amount_paid

#     def clean_discount(self):
#         discount = self.cleaned_data.get('discount', 0)
#         if self.instance.discount_used and discount != 0:
#             raise forms.ValidationError("Discount has already been applied and cannot be edited.")
#         return discount

from django import forms
from django.utils import timezone
from .models import ServiceApplication

class ServiceApplicationPaymentForm(forms.ModelForm):
    ACTION_CHOICES = [
        ('payment_pending', 'পেমেন্ট যাচাই চলমান'),
        ('partial_payment', 'আংশিক পেমেন্ট সম্পন্ন'),
        ('full_payment', 'পেমেন্ট পরিশোধ হয়েছে'),
        ('rejected', 'পেমেন্ট বাতিল হয়েছে'),
    ]

    action_taken = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    due_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="বাকি পরিমাণ",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    payment_due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date(),
        required=False
    )

    class Meta:
        model = ServiceApplication
        fields = [
            'status',
            'amount_paid',
            'payment_message',
            'discount',
            'action_taken',
            'payment_due_date'
        ]

        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['amount_paid'].required = False
        if self.instance:
            self.fields['amount_paid'].initial = self.instance.balance
            self.fields['due_amount'].initial = self.instance.balance

    def clean_amount_paid(self):
        amount_paid = self.cleaned_data.get('amount_paid')
        if amount_paid in [None, '']:
            return self.instance.balance
        return amount_paid

    def clean_discount(self):
        discount = self.cleaned_data.get('discount', 0)
        if discount < 0:
            raise forms.ValidationError("ডিসকাউন্ট ঋণাত্মক হতে পারে না।")
        return discount






# Client Pay from their id    -    service_application_payment.html   -    ServiceApplicationPaymentView
# path('client-payment/<int:service_application_id>/', login_required(ServiceApplicationPaymentView.as_view()), name='service_application_payment')

from .models import ClientPayment

class ClientPaymentForm(forms.ModelForm):
    class Meta:
        model = ClientPayment
        fields = ['amount', 'payment_method', 'transaction_id', 'message', 'image']

    amount = forms.IntegerField(required=True, label="পেমেন্ট পরিমাণ")
    payment_method = forms.ChoiceField(
        choices=ClientPayment.PAYMENT_METHOD_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="পেমেন্ট পদ্ধতি"
    )
    transaction_id = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="লেনদেন আইডি (যদি থাকে)"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label="বার্তা (যদি থাকে)"
    )
    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="পেমেন্ট প্রমাণ চিত্র"
    )



# Admin approval form for client payment

from django import forms
from .models import ClientPayment

class ClientPaymentAdminForm(forms.ModelForm):
    class Meta:
        model = ClientPayment
        fields = [
            'amount',
            'payment_method',
            'transaction_id',
            'message',
            'status',
            'admin_message',
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }




# Admin edit for timeline and message
from apps.services.models import ServiceApplicationProgress

class ServiceApplicationProgressForm(forms.ModelForm):
    class Meta:
        model = ServiceApplicationProgress
        fields = ['status', 'message']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# Admin discount form

from .models import ServiceApplication

class ServiceApplicationDiscountForm(forms.ModelForm):
    class Meta:
        model = ServiceApplication
        fields = ['discount']
        widgets = {
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter discount amount'
            }),
        }
        labels = {
            'discount': 'ডিসকাউন্ট (৳)',
        }






# Notice Form

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['service', 'title', 'message', 'file', 'image', 'status']


class PublicNoticeForm(forms.ModelForm):
    class Meta:
        model = NoticePublic
        fields = [ 'title', 'message', 'file', 'image', 'status']
