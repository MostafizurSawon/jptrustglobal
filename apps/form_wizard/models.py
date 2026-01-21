from django.db import models
from django.conf import settings

# Choices for various fields
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('Other', 'Other'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

MARRIED_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

EDUCATION_CHOICES = [
    ('SSC', 'SSC'),
    ('HSC', 'HSC'),
    ('HONOURS', 'Honours'),
    ('Others', 'Others'),
]

class TravelAgencyCV(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cv')

    # General Info
    full_name = models.CharField("Full Name (English)", max_length=200)
    full_name_bn = models.CharField("Full Name (Bangla)", max_length=200, blank=True)
    bio = models.TextField(blank=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='Other')
    language = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.IntegerField(unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male")

    # Parent Info
    fathers_name = models.CharField(max_length=200, blank=True, null=True)
    fathers_mobile = models.CharField(max_length=20, blank=True, null=True)
    fathers_nid = models.CharField(max_length=20, blank=True, null=True)

    mothers_name = models.CharField(max_length=200, blank=True, null=True)
    mothers_mobile = models.CharField(max_length=20, blank=True, null=True)
    mothers_nid = models.CharField(max_length=20, blank=True, null=True)


    # Academic Info
    last_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='SSC', blank=True, null=True)
    last_education_other = models.CharField(max_length=100, blank=True, null=True)
    last_education_result = models.CharField(max_length=100, blank=True, null=True)
    last_education_passing_year = models.PositiveIntegerField(blank=True, null=True)


    # Address Info
    wardNo = models.IntegerField(null=True, blank=True)
    postOffice = models.CharField(max_length=50, null=True, blank=True)
    policeStation = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    permanent_address_same = models.BooleanField(default=False)
    permanent_wardNo = models.IntegerField(null=True, blank=True)
    permanent_postOffice = models.CharField(max_length=50, null=True, blank=True)
    permanent_policeStation = models.CharField(max_length=50, null=True, blank=True)
    permanent_district = models.CharField(max_length=50, null=True, blank=True)
    permanent_postal_code = models.IntegerField(null=True, blank=True)


    # Skill Info
    current_job_status = models.CharField(max_length=20, choices=[('Student', 'Student'), ('Employed', 'Employed'), ('Unemployed', 'Unemployed')], blank=True, null=True)
    skills = models.CharField(max_length=200, null=True, blank=True)
    special_skills = models.CharField(max_length=200, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number}'s CV"












class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# class GuestCV(models.Model):
#     BLOOD_GROUP_CHOICES = [
#         ('A+', 'A+'), ('A-', 'A-'),
#         ('AB+', 'AB+'), ('AB-', 'AB-'),
#         ('B+', 'B+'), ('B-', 'B-'),
#         ('O+', 'O+'), ('O-', 'O-'),
#         ('Other', 'Other'),
#     ]

#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other'),
#     ]

#     MARRIED_CHOICES = [
#         ('Yes', 'Yes'),
#         ('No', 'No'),
#     ]

#     EDUCATION_CHOICES = [
#         ('SSC', 'SSC'),
#         ('HSC', 'HSC'),
#         ('HONOURS', 'Honours'),
#         ('Others', 'Others'),
#     ]

#     JOB_STATUS_CHOICES = [
#         ('Unemployed', 'Unemployed'),
#         ('Employed', 'Employed'),
#         ('Student', 'Student'),
#         ('Others', 'Others'),
#     ]

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guest_cv')

#     # Name
#     full_name = models.CharField("Full Name (English)", max_length=200)
#     full_name_bn = models.CharField("Full Name (Bangla)", max_length=200, blank=True)

#     # Skills
#     skills = models.CharField(max_length=200, null=True, blank=True, help_text="Your main skill or expertise")
#     special_skills = models.CharField(max_length=200, null=True, blank=True, help_text="Any special skills you have")
#     bio = models.TextField(blank=True, help_text="A brief introduction about yourself")

#     # Blood Group
#     blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='Other')
#     blood_group_other = models.CharField(max_length=20, blank=True, help_text="If Other, specify here")

#     # Photo
#     profile_picture = models.ImageField(upload_to='cv_pictures/', null=True, blank=True)

#     # Languages
#     languages = models.ManyToManyField(Language, blank=True, related_name='cvs')
#     language_other = models.CharField(max_length=255, blank=True, help_text="If Other, specify additional languages here")

#     # Contact & Personal info
#     email = models.EmailField(blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     nationality = models.CharField(max_length=100, blank=True, null=True)
#     national_id = models.IntegerField(unique=True, blank=True, null=True, help_text="National ID")

#     # Addresses
#     current_address = models.TextField(blank=True, null=True)
#     is_permanent_same_as_current = models.BooleanField(default=False)
#     permanent_address = models.TextField(blank=True, null=True)

#     # Family info
#     fathers_name = models.CharField(max_length=200, blank=True, null=True)
#     fathers_mobile = models.CharField(max_length=20, blank=True, null=True)
#     fathers_nid = models.CharField(max_length=20, blank=True, null=True)

#     mothers_name = models.CharField(max_length=200, blank=True, null=True)
#     mothers_mobile = models.CharField(max_length=20, blank=True, null=True)
#     mothers_nid = models.CharField(max_length=20, blank=True, null=True)

#     # Other personal info
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male', blank=True, null=True)
#     married = models.CharField(max_length=5, choices=MARRIED_CHOICES, default='No', blank=True, null=True)

#     # Education
#     last_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='SSC', blank=True, null=True)
#     last_education_other = models.CharField(max_length=100, blank=True, null=True, help_text="If Others, specify here")
#     last_education_result = models.CharField(max_length=100, blank=True, null=True)
#     last_education_passing_year = models.PositiveIntegerField(blank=True, null=True)

#     # Job info
#     current_job_status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='Unemployed', blank=True, null=True)
#     current_job_status_other = models.CharField(max_length=100, blank=True, null=True, help_text="If Others, specify here")
#     current_job_title = models.CharField(max_length=200, blank=True, null=True)

#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.full_name}'s CV"

# active cv this

class GuestCV(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    GENDER_CHOICES = [
        ('Male', 'পুরুষ'),
        ('Female', 'নারী'),
        ('Other', 'অন্যান্য'),
    ]

    MARRIED_CHOICES = [
    ('Married', 'বিবাহিত'),
    ('Unmarried', 'অবিবাহিত'),
]


    EDUCATION_CHOICES = [
        ('SSC', 'এসএসসি'),
        ('HSC', 'এইচএসসি'),
        ('HONOURS', 'স্নাতক'),
        ('Others', 'অন্যান্য'),
    ]

    JOB_STATUS_CHOICES = [
        ('Unemployed', 'বেকার'),
        ('Employed', 'চাকরিজীবী'),
        ('Student', 'ছাত্র/ছাত্রী'),
        ('Business', 'ব্যবসা'),
        ('Others', 'অন্যান্য'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guest_cv', null=True, blank=True)

    full_name = models.CharField("পূর্ণ নাম (ইংরেজি)", max_length=100, blank=True)
    full_name_bn = models.CharField("পূর্ণ নাম (বাংলা)", max_length=100, blank=True)

    skills = models.CharField("দক্ষতা", max_length=200, null=True, blank=True, help_text="মূল দক্ষতা")
    special_skills = models.CharField("বিশেষ দক্ষতা", max_length=200, null=True, blank=True, help_text="বিশেষ কোনো দক্ষতা থাকলে")
    bio = models.TextField("জীবনবৃত্তান্ত", blank=True, help_text="সংক্ষিপ্ত নিজের পরিচয়")

    blood_group = models.CharField("রক্তের গ্রুপ", max_length=10, choices=BLOOD_GROUP_CHOICES, default='Other')

    profile_picture = models.ImageField("প্রোফাইল ছবি", upload_to='agent/client/cv_pictures/', null=True, blank=True)

    language = models.CharField("ভাষা", max_length=255, blank=True)

    email = models.EmailField("ইমেইল", blank=True, null=True)
    date_of_birth = models.DateField("জন্মতারিখ", blank=True, null=True)
    nationality = models.CharField("জাতীয়তা", max_length=100, blank=True, null=True)
    national_id = models.IntegerField("জাতীয় পরিচয়পত্র নম্বর", unique=True, blank=True, null=True, help_text="জাতীয় পরিচয়পত্র নম্বর")

    current_address = models.TextField("বর্তমান ঠিকানা", blank=True, null=True)
    is_permanent_same_as_current = models.BooleanField("স্থায়ী ঠিকানা একই?", default=False)
    permanent_address = models.TextField("স্থায়ী ঠিকানা", blank=True, null=True)

    fathers_name = models.CharField("পিতার নাম", max_length=200, blank=True, null=True)
    fathers_mobile = models.CharField("পিতার মোবাইল", max_length=20, blank=True, null=True)
    fathers_nid = models.CharField("পিতার এনআইডি", max_length=20, blank=True, null=True)

    mothers_name = models.CharField("মাতার নাম", max_length=200, blank=True, null=True)
    mothers_mobile = models.CharField("মাতার মোবাইল", max_length=20, blank=True, null=True)
    mothers_nid = models.CharField("মাতার এনআইডি", max_length=20, blank=True, null=True)

    gender = models.CharField("লিঙ্গ", max_length=10, choices=GENDER_CHOICES, default='Male', blank=True, null=True)
    married = models.CharField("বৈবাহিক অবস্থা", max_length=10, choices=MARRIED_CHOICES, default='Unmarried', blank=True, null=True)

    last_education = models.CharField("সর্বশেষ শিক্ষাগত যোগ্যতা", max_length=20, choices=EDUCATION_CHOICES, default='SSC', blank=True, null=True)
    last_education_result = models.CharField("ফলাফল", max_length=100, blank=True, null=True)
    last_education_passing_year = models.PositiveIntegerField("পাসের বছর", blank=True, null=True)

    current_job_status = models.CharField("বর্তমান পেশার অবস্থা", max_length=20, choices=JOB_STATUS_CHOICES, default='Unemployed', blank=True, null=True)

    created_at = models.DateTimeField("তৈরির তারিখ", auto_now_add=True)
    updated_at = models.DateTimeField("আপডেটের তারিখ", auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s CV"





class PassportInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passport_info')

    profile_photo = models.ImageField(upload_to='passport_photo', null=True, blank=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, default='Bangladeshi', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'পুরুষ'), ('Female', 'মহিলা'), ('Other', 'অন্যান্য')], null=True, blank=True)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    mother_name = models.CharField(max_length=200, null=True, blank=True)
    spouse_name = models.CharField(max_length=200, blank=True, null=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    place_of_issue = models.CharField(max_length=100, null=True, blank=True)
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

    # Additional file fields (1 to 6)
    additional_file_1 = models.FileField(upload_to='passport/passport_additional_files/', null=True, blank=True)
    additional_file_2 = models.FileField(upload_to='passport/passport_additional_files/', null=True, blank=True)
    additional_file_3 = models.FileField(upload_to='passport/passport_additional_files/', null=True, blank=True)
    additional_file_4 = models.FileField(upload_to='passport/passport_additional_files/', null=True, blank=True)
    additional_file_5 = models.FileField(upload_to='passport/passport_additional_files/', null=True, blank=True)
    additional_file_6 = models.FileField(upload_to='passport/passport_additional_files/', null=True, blank=True)


    # Correct reference to AgentInfo with the full app path
    # agent = models.ForeignKey(
    #     'accounts.AgentInfo',  # Correctly reference 'AgentInfo' from the 'accounts' app
    #     on_delete=models.SET_NULL,  # Set to NULL if agent is deleted
    #     null=True,  # Make it nullable as not all users will be agents
    #     blank=True,  # Blank is allowed for users who are not agents
    #     related_name='passport_info_agent',  # Allows reverse lookup
    # )

    def __str__(self):
        return f"{self.user.phone_number}'s Passport Info"
