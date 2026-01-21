from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'purpose', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'contact-input form-control', 'placeholder': 'আপনার সম্পূর্ণ নাম'}),
            'email': forms.EmailInput(attrs={'class': 'contact-input form-control', 'placeholder': 'আপনার ইমেইল (যদি থাকে)'}),
            'phone': forms.TextInput(attrs={'class': 'contact-input form-control', 'placeholder': 'আপনার ফোন নম্বর'}),
            'purpose': forms.Select(attrs={'class': 'form-select form-control', 'placeholder': 'যোগাযোগের কারণ'}),
            'message': forms.Textarea(attrs={'class': 'contact-input form-control', 'rows': 4, 'placeholder': 'আপনার মেসেজ',}),
        }


from django import forms
from .models import Contact

class ContactForm2(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'purpose', 'message']




class ContactNoteForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'নোট লিখুন...',
            }),
        }





# Site Settings

from .models import SiteSettings, Slider

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Title'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whatsapp'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 4}),
            'trending': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Trending Description', 'rows': 4}),
            'service': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Service Description', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'map_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Map Link URL'}),
            'footer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Footer Text'}),
            'footer_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Footer Description'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram URL'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Youtube URL'}),
            'x': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'X URL'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'favicon': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        widgets = {
            'carousel_1_heading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শিরোনাম ১'}),
            'carousel_1_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বর্ণনা ১'}),
            'carousel_1_button_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'বাটন লিংক ১'}),

            'carousel_2_heading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শিরোনাম ২'}),
            'carousel_2_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বর্ণনা ২'}),
            'carousel_2_button_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'বাটন লিংক ২'}),

            'carousel_3_heading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শিরোনাম ৩'}),
            'carousel_3_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বর্ণনা ৩'}),
            'carousel_3_button_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'বাটন লিংক ৩'}),

            'carousel_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'carousel_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'carousel_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


from .models import Services, ServiceDescription, Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'image', 'description', 'ratings']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ratings': forms.Select(attrs={'class': 'form-select'}),
        }


from django import forms
from .models import Services, ServiceDescription, Team

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter service name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter service description', 'rows': 3})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class ServiceDescriptionForm(forms.ModelForm):
    class Meta:
        model = ServiceDescription
        fields = ['sv_description']

    def __init__(self, *args, **kwargs):
        super(ServiceDescriptionForm, self).__init__(*args, **kwargs)
        self.fields['sv_description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4})



from .models import Trending

class TrendingForm(forms.ModelForm):
    class Meta:
        model = Trending
        fields = ['name', 'description', 'image', 'link']

    def __init__(self, *args, **kwargs):
        super(TrendingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 3})



# Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'image', 'designation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team member name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
        }



# Appointment Forms
from django import forms
from .models import Appointment
import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'address', 'mobile_number', 'appointment_date', 'description', 'status', 'note']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার নাম লিখুন'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ঠিকানা লিখুন', 'rows': 3}),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '০১XXXXXXXXX',
                'pattern': r'^0\d{10}$'
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'বিবরণ লিখুন', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'নোট (ঐচ্ছিক)'}),
        }

class AppointmentFormPublic(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'address', 'mobile_number', 'appointment_date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'আপনার নাম লিখুন'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ঠিকানা লিখুন', 'rows': 3}),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '০১XXXXXXXXX',
                'pattern': r'^0\d{10}$'
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'বিবরণ লিখুন', 'rows': 3}),
        }


# Appointment er notice er warning lekha
from .models import AppointmentNotice

class AppointmentNoticeForm(forms.ModelForm):
    class Meta:
        model = AppointmentNotice
        fields = ['title1', 'des1', 'title2', 'des2', 'title3', 'des3']
        labels = {
            'title1': 'শিরোনাম ১',
            'des1': 'বর্ণনা ১',
            'title2': 'শিরোনাম ২',
            'des2': 'বর্ণনা ২',
            'title3': 'শিরোনাম ৩',
            'des3': 'বর্ণনা ৩',
        }
        widgets = {
            'title1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শিরোনাম ১ লিখুন'}),
            'des1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'বর্ণনা ১ লিখুন', 'rows': 3}),
            'title2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শিরোনাম ২ লিখুন'}),
            'des2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'বর্ণনা ২ লিখুন', 'rows': 3}),
            'title3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'শিরোনাম ৩ লিখুন'}),
            'des3': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'বর্ণনা ৩ লিখুন', 'rows': 3}),
        }




# Cv Form
from .models import Cv

class CvForm(forms.ModelForm):
    class Meta:
        model = Cv
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CvForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        for desc_field in ['des1', 'des2']:
            if desc_field in self.fields:
                self.fields[desc_field].widget.attrs.update({
                    'rows': 2,
                    'style': 'resize: vertical; min-height: 60px;'
                })



# Choose us
from .models import Choose

class ChooseForm(forms.ModelForm):
    class Meta:
        model = Choose
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ChooseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Specific textarea fields to auto-resize
        for desc_field in ['des1', 'des2', 'des3', 'des4']:
            if desc_field in self.fields:
                self.fields[desc_field].widget.attrs.update({
                    'id': f'id_{desc_field}',
                    'rows': 2,
                    'style': 'resize: vertical; min-height: 60px;'
                })
