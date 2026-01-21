from django import forms
from .models import ClientCvAgent

class ClientCvAgentForm(forms.ModelForm):
    class Meta:
        model = ClientCvAgent
        exclude = ['agent', 'created_at', 'updated_at', 'blood_group_other']  # agent handled in view
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name_bn': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'special_skills': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'blood_group_other': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_permanent_same_as_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fathers_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'fathers_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'married': forms.Select(attrs={'class': 'form-select'}),
            'last_education': forms.Select(attrs={'class': 'form-select'}),
            'last_education_other': forms.TextInput(attrs={'class': 'form-control'}),
            'last_education_result': forms.TextInput(attrs={'class': 'form-control'}),
            'last_education_passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_job_status': forms.Select(attrs={'class': 'form-select'}),
        }
