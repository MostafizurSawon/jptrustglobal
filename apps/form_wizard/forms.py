# Not
from django import forms
from .models import TravelAgencyCV

class CVForm(forms.ModelForm):
    class Meta:
        model = TravelAgencyCV
        fields = [
            'full_name', 'full_name_bn', 'bio', 'blood_group', 'language',
            'email', 'date_of_birth', 'nationality', 'national_id', 'gender',
            'fathers_name', 'fathers_mobile', 'fathers_nid',
            'mothers_name', 'mothers_mobile', 'mothers_nid',
            'last_education', 'last_education_other', 'last_education_result', 'last_education_passing_year',
            'wardNo', 'postOffice', 'policeStation', 'district', 'postal_code',
            'permanent_address_same', 'permanent_wardNo', 'permanent_postOffice', 'permanent_policeStation',
            'permanent_district', 'permanent_postal_code', 'current_job_status', 'skills', 'special_skills'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding date format for 'date_of_birth' field
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})




from .models import GuestCV, Language
from django_select2.forms import Select2TagWidget


class TravelAgencyCVForm(forms.ModelForm):
    class Meta:
        model = GuestCV
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name_bn': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'special_skills': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
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
            'last_education_result': forms.TextInput(attrs={'class': 'form-control'}),
            'last_education_passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_job_status': forms.Select(attrs={'class': 'form-select'}),
        }

# class TravelAgencyCVForm(forms.ModelForm):
#     languages = forms.ModelMultipleChoiceField(
#         queryset=Language.objects.all(),
#         required=False,
#         label='Languages',
#         widget=Select2TagWidget(attrs={'class': 'form-control', 'style': 'width:100%;', 'data-tags': 'true'})
#     )

#     class Meta:
#         model = GuestCV
#         exclude = ['user','is_permanent_same_as_current']
#         widgets = {
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'full_name_bn': forms.TextInput(attrs={'class': 'form-control'}),
#             'skills': forms.TextInput(attrs={'class': 'form-control'}),
#             'special_skills': forms.TextInput(attrs={'class': 'form-control'}),
#             'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'blood_group': forms.Select(attrs={'class': 'form-select'}),
#             'blood_group_other': forms.TextInput(attrs={'class': 'form-control'}),
#             'language_other': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'nationality': forms.TextInput(attrs={'class': 'form-control'}),
#             'national_id': forms.NumberInput(attrs={'class': 'form-control'}),
#             'current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             # 'is_permanent_same_as_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'fathers_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'fathers_mobile': forms.TextInput(attrs={'class': 'form-control'}),
#             'fathers_nid': forms.TextInput(attrs={'class': 'form-control'}),
#             'mothers_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'mothers_mobile': forms.TextInput(attrs={'class': 'form-control'}),
#             'mothers_nid': forms.TextInput(attrs={'class': 'form-control'}),
#             'gender': forms.Select(attrs={'class': 'form-select'}),
#             'married': forms.Select(attrs={'class': 'form-select'}),
#             'last_education': forms.Select(attrs={'class': 'form-select'}),
#             'last_education_other': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_education_result': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_education_passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
#             'current_job_status': forms.Select(attrs={'class': 'form-select'}),
#             'current_job_status_other': forms.TextInput(attrs={'class': 'form-control'}),
#             'current_job_title': forms.TextInput(attrs={'class': 'form-control'}),
#             'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     blood_group = cleaned_data.get('blood_group')
    #     if blood_group == 'Other' and not cleaned_data.get('blood_group_other'):
    #         self.add_error('blood_group_other', 'Please specify your blood group.')

    #     selected_languages = cleaned_data.get('languages')
    #     if selected_languages and any(lang.name == 'Other' for lang in selected_languages):
    #         if not cleaned_data.get('language_other'):
    #             self.add_error('language_other', 'Please specify the other language.')

    #     if cleaned_data.get('is_permanent_same_as_current'):
    #         cleaned_data['permanent_address'] = cleaned_data.get('current_address')

    #     if cleaned_data.get('current_job_status') in ['Employed', 'Others'] and not cleaned_data.get('current_job_title'):
    #         self.add_error('current_job_title', 'Please provide your job title.')

    #     if cleaned_data.get('last_education') == 'Others' and not cleaned_data.get('last_education_other'):
    #         self.add_error('last_education_other', 'Please specify your education.')

    #     if cleaned_data.get('current_job_status') == 'Others' and not cleaned_data.get('current_job_status_other'):
    #         self.add_error('current_job_status_other', 'Please specify your job status.')

    #     return cleaned_data






# without agent
from django import forms
from .models import PassportInfo

class PassportInfoForm(forms.ModelForm):
    class Meta:
        model = PassportInfo
        fields = [
            'profile_photo', 'passport_number', 'full_name', 'date_of_birth', 'place_of_birth', 'nationality', 'gender',
            'father_name', 'mother_name', 'spouse_name', 'issue_date', 'expiry_date', 'place_of_issue',
            'passport_photo', 'signature',
            'additional_file_1', 'additional_file_2', 'additional_file_3',
            'additional_file_4', 'additional_file_5', 'additional_file_6',
        ]

        widgets = {
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'পাসপোর্ট নম্বর দিন'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'পূর্ণ নাম দিন'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'জন্ম তারিখ দিন'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'জন্মস্থান দিন'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'জাতীয়তা দিন'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বাবার নাম দিন'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'মায়ের নাম দিন'}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'স্বামী/স্ত্রীর নাম দিন'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'পাসপোর্ট ইস্যু তারিখ দিন'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'পাসপোর্ট মেয়াদ শেষ হওয়ার তারিখ দিন'}),
            'place_of_issue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'পাসপোর্ট ইস্যুর স্থান দিন'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'passport_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'signature': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_file_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_file_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_file_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_file_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_file_5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_file_6': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop user out of kwargs
        super().__init__(*args, **kwargs)





# from django import forms
# from .models import PassportInfo, AgentInfo

# class PassportInfoForm(forms.ModelForm):
#     class Meta:
#         model = PassportInfo
#         fields = ['profile_photo', 'passport_number', 'full_name', 'date_of_birth', 'place_of_birth', 'nationality', 'gender',
#                   'father_name', 'mother_name', 'spouse_name', 'issue_date', 'expiry_date', 'place_of_issue', 'passport_photo', 'signature', 'agent']

#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#         }

#     agent = forms.ModelChoiceField(
#         queryset=AgentInfo.objects.all(),
#         required=False,  # Only show the agent field if the user is an agent
#         empty_label="Select Agent",
#         widget=forms.Select(attrs={'class': 'form-select'})
#     )

#     def __init__(self, *args, **kwargs):
#         # Accept 'user' in kwargs
#         self.user = kwargs.pop('user', None)  # Pop user out of kwargs
#         super().__init__(*args, **kwargs)

#         # Filter agent choices based on the logged-in user
#         if self.user and self.user.role == 'agent':
#             self.fields['agent'].queryset = AgentInfo.objects.filter(user=self.user)



# class PassportInfoForm(forms.ModelForm):
#     class Meta:
#         model = PassportInfo
#         fields = ['profile_photo', 'passport_number', 'full_name', 'date_of_birth', 'place_of_birth', 'nationality', 'gender',
#                   'father_name', 'mother_name', 'spouse_name', 'issue_date', 'expiry_date', 'place_of_issue', 'passport_photo', 'signature', 'agent']

#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#         }

#     agent = forms.ModelChoiceField(
#         queryset=AgentInfo.objects.all(),
#         required=False,  # Only show the agent field if the user is an agent
#         empty_label="Select Agent",
#         widget=forms.Select(attrs={'class': 'form-select'})
#     )

#     def __init__(self, *args, **kwargs):
#         # Accept 'user' in kwargs
#         self.user = kwargs.pop('user', None)  # Pop user out of kwargs
#         super().__init__(*args, **kwargs)

#         # Filter agent choices based on the logged-in user
#         if self.user and self.user.role == 'agent':
#             self.fields['agent'].queryset = AgentInfo.objects.filter(user=self.user)
