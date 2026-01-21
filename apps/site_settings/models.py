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
        ('study_visa', 'Study visa'),
        ('work_visa', 'Work visa'),
        ('tourist_visa', 'Tourist visa'),
        ('agent_interest', 'Agent interest'),
        ('general', 'General Question'),
        ('other', 'Other '),
    ], default='general', null=True, blank=True)
    message = models.TextField()
    note = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name_part = self.name if self.name else "Unnamed Contact"
        purpose_part = self.get_purpose_display() if self.purpose else "No Purpose"
        return f"{name_part} ({purpose_part})"



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
    carousel_1 = models.ImageField(
        upload_to='site_settings/sliders/',
        blank=True,
        null=True,
        verbose_name="Slide 1 - Image"
    )
    carousel_1_heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Slide 1 - Main Heading"
    )
    carousel_1_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Slide 1 - Subtext / Description"
    )
    carousel_1_button_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Slide 1 - Button URL"
    )

    # Carousel 2
    carousel_2 = models.ImageField(
        upload_to='site_settings/sliders/',
        blank=True,
        null=True,
        verbose_name="Slide 2 - Image"
    )
    carousel_2_heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Slide 2 - Main Heading"
    )
    carousel_2_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Slide 2 - Subtext / Description"
    )
    carousel_2_button_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Slide 2 - Button URL"
    )

    # Carousel 3
    carousel_3 = models.ImageField(
        upload_to='site_settings/sliders/',
        blank=True,
        null=True,
        verbose_name="Slide 3 - Image"
    )
    carousel_3_heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Slide 3 - Main Heading"
    )
    carousel_3_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Slide 3 - Subtext / Description"
    )
    carousel_3_button_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Slide 3 - Button URL"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Homepage Slider Settings"




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
        message="Phone number must start with '0' followed by 10 digits (total 11 digits)."
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Full Name"
    )
    address = models.TextField(
        verbose_name="Full Address"
    )
    mobile_number = models.CharField(
        max_length=11,
        validators=[phone_validator],
        help_text="Format: 01XXXXXXXXX (must be 11 digits starting with 0)",
        verbose_name="Mobile Number"
    )
    appointment_date = models.DateField(
        verbose_name="Preferred Appointment Date"
    )
    description = models.TextField(
        verbose_name="Purpose of Appointment / Details"
    )

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Appointment Status"
    )

    note = models.TextField(
        null=True,
        blank=True,
        verbose_name="Admin Notes / Remarks"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return f"{self.name} - {self.appointment_date.strftime('%Y-%m-%d')}"


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
