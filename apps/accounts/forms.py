from django import forms
from .models import AgentInfo, User
from django.forms import DateInput

class AgentInfoForm(forms.ModelForm):
    class Meta:
        model = AgentInfo
        fields = ['user', 'full_name','image', 'date_of_birth', 'address', 'city', 'country', 'job_title', 'status']

    # DateInput widget for date of birth field
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    # Override the user field to filter users by role "agent"
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='agent'),  # Only show users with the role 'agent'
        required=True,
        empty_label="Select Agent"  # Optional: to hide the "--------" option
    )


# admin edit agent form

class AgentInfoEditForm(forms.ModelForm):
    class Meta:
        model = AgentInfo
        fields = ['full_name','image', 'date_of_birth', 'address', 'city', 'country', 'job_title', 'status']  # Excluding the user field

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    # Status is editable for admin/HR
    status = forms.ChoiceField(
        choices=AgentInfo.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )




class AgentInfoFormDashboard(forms.ModelForm):
    class Meta:
        model = AgentInfo
        fields = ['full_name','image', 'date_of_birth', 'address', 'city', 'country', 'job_title']

    # Add a custom widget for date_of_birth to render it as a date input
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Using the date input type
    )

    # You can add any custom validation here if needed
    # Example: Ensure that the agent's full name is provided
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise forms.ValidationError("Full name is required.")
        return full_name
