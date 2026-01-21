from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Contact(models.Model):
    phone_validator = RegexValidator(
        regex=r'^0\d{10}$',
        message="Phone number must start with '0' and be exactly 11 digits long."
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        max_length=11,
        validators=[phone_validator],
        help_text="Phone number must start with 0 and be exactly 11 digits."
    )
    purpose = models.CharField(max_length=255, choices=[
        ('study_visa', 'স্টাডি ভিসা'),
        ('work_visa', 'ওয়ার্ক পারমিট ভিসা'),
        ('tourist_visa', 'ট্যুরিস্ট ভিসা'),
        ('agent_interest', 'এজেন্ট হতে আগ্রহী'),
        ('general', 'সাধারণ প্রশ্ন'),
        ('other', 'অন্যান্য '),
    ], default='general', null=True, blank=True)
    message = models.TextField()
    note = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name_part = self.name if self.name else "Unnamed Contact"
        purpose_part = self.get_purpose_display() if self.purpose else "No Purpose"
        return f"{name_part} ({purpose_part})"




# from django.db import models
# from django.core.validators import RegexValidator

# # Create your models here.
# class Contact(models.Model):
#     phone_validator = RegexValidator(
#         regex=r'^0\d{10}$',
#         message="Phone number must start with '0' and be exactly 11 digits long."
#     )
#     name = models.CharField(max_length=100)
#     email = models.EmailField(blank=True, null=True)
#     phone = models.CharField(
#         max_length=11,
#         validators=[phone_validator],
#         help_text="Phone number must start with 0 and be exactly 11 digits."
#     )
#     purpose = models.CharField(max_length=255, choices=[
#         ('general', 'সাধারণ প্রশ্ন'),
#         ('booking', 'বুকিং'),
#         ('feedback', 'মতামত'),
#         ('other', 'অন্যান্য '),
#     ], default='general', null=True, blank=True)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         name_part = self.name if self.name else "Unnamed Contact"
#         purpose_part = self.get_purpose_display() if self.purpose else "No Purpose"
#         return f"{name_part} ({purpose_part})"



class SiteSettings(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    trending = models.TextField(null=True, blank=True)
    service = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    # Link to MediaFiles by category (one per category)
    logo = models.ImageField(upload_to='site_settings/logo_fav/', blank=True, null=True, verbose_name="site_logo")
    favicon = models.ImageField(upload_to='site_settings/logo_fav/', blank=True, null=True, verbose_name="site_fav")


    # Contact Info
    phone = models.CharField(max_length=18, blank=True, null=True)
    whatsapp = models.CharField(max_length=18,blank=True,null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    map_link = models.URLField(null=True, blank=True)

    # Footer Info
    footer = models.CharField(max_length=255, blank=True)
    footer_description = models.CharField(max_length=255, blank=True)

    # Social Links
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Slider(models.Model):
    # Carousel 1
    carousel_1 = models.ImageField(upload_to='site_settings/sliders/', blank=True, null=True, verbose_name="স্লাইড ১ ইমেজ")
    carousel_1_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="স্লাইড ১ শিরোনাম")
    carousel_1_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="স্লাইড ১ বিবরণ")
    carousel_1_button_link = models.URLField(blank=True, null=True, verbose_name="স্লাইড ১ লিংক")

    # Carousel 2
    carousel_2 = models.ImageField(upload_to='site_settings/sliders/', blank=True, null=True, verbose_name="স্লাইড ২ ইমেজ")
    carousel_2_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="স্লাইড ২ শিরোনাম")
    carousel_2_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="স্লাইড ২ বিবরণ")
    carousel_2_button_link = models.URLField(blank=True, null=True, verbose_name="স্লাইড ২ লিংক")

    # Carousel 3
    carousel_3 = models.ImageField(upload_to='site_settings/sliders/', blank=True, null=True, verbose_name="স্লাইড ৩ ইমেজ")
    carousel_3_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="স্লাইড ৩ শিরোনাম")
    carousel_3_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="স্লাইড ৩ বিবরণ")
    carousel_3_button_link = models.URLField(blank=True, null=True, verbose_name="স্লাইড ৩ লিংক")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "হোমপেজ স্লাইডার কনফিগারেশন"




# Service Section

class Services(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='site_settings/services/', blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Service"

# Trending Video

class Trending(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='site_settings/trending/', blank=True, null=True)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Service"


# Our Team

class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='site_settings/our_team/', blank=True, null=True)
    designation = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Team"

# Testimonals Section

class Testimonial(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='site_settings/testimoinals/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ratings = models.CharField(max_length=10, choices=[
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars'),
    ], default='5')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Testimonial"


class ServiceDescription(models.Model):
    sv_description = models.TextField(blank=True, null=True)

    def __str__(self):
        # return self.sv_description[:50] if self.sv_description else "No Description"
        return self.sv_description if self.sv_description else "No Description"


# Appointment Model
class Appointment(models.Model):
    phone_validator = RegexValidator(
        regex=r'^0\d{10}$',
        message="Phone number must start with '0' and be exactly 11 digits long."
    )

    name = models.CharField(max_length=100, verbose_name="নাম")
    address = models.TextField(verbose_name="ঠিকানা")
    mobile_number = models.CharField(
        max_length=11,
        validators=[phone_validator],
        help_text="মোবাইল নম্বর অবশ্যই ০ দিয়ে শুরু হতে হবে এবং ১১ ডিজিটের হতে হবে।",
        verbose_name="মোবাইল নম্বর"
    )
    appointment_date = models.DateField(verbose_name="অ্যাপয়েন্টমেন্টের তারিখ")
    description = models.TextField(verbose_name="বিবরণ")

    STATUS_CHOICES = [
        ('pending', 'পেন্ডিং'),
        ('confirmed', 'নিশ্চিত'),
        ('completed', 'সম্পন্ন'),
        ('cancelled', 'বাতিল'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="অবস্থা")

    note = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.appointment_date}"


# Frontend Appointment Notice
class AppointmentNotice(models.Model):
    title1= models.CharField(max_length=100, null=True, blank=True)
    des1= models.TextField(null=True)
    title2= models.CharField(max_length=100, null=True, blank=True)
    des2= models.TextField(null=True)
    title3= models.CharField(max_length=100, null=True, blank=True)
    des3= models.TextField(null=True)

    def __str__(self):
        return f"{self.title1}"


# Frontend cv Section

class Cv(models.Model):
    link=models.URLField(null=True, blank= True)
    title=models.CharField(max_length=250, null=True, blank=True)
    title_d=models.CharField(max_length=250, null=True, blank=True)
    img1=models.ImageField(upload_to='site_settings/cv/', blank=True, null=True)
    title1=models.CharField(max_length=250, null=True, blank=True)
    des1=models.TextField(null=True, blank= True)
    img2=models.ImageField(upload_to='site_settings/cv/', blank=True, null=True)
    title2=models.CharField(max_length=250, null=True, blank=True)
    des2=models.TextField(null=True, blank= True)

    def __str__(self):
        return f"{self.title}"


class Choose(models.Model):
    image = models.ImageField(upload_to='site_settings/chose/', blank=True, null=True)
    des1=models.TextField(null=True, blank= True)
    img1=models.ImageField(upload_to='site_settings/chose/', blank=True, null=True)
    des2=models.TextField(null=True, blank= True)
    img2=models.ImageField(upload_to='site_settings/chose/', blank=True, null=True)
    des3=models.TextField(null=True, blank= True)
    img3=models.ImageField(upload_to='site_settings/chose/', blank=True, null=True)
    des4=models.TextField(null=True, blank= True)
    img4=models.ImageField(upload_to='site_settings/chose/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
