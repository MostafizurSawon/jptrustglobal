from django.db import models

class ClientCvAgent(models.Model):
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
        ('Yes', 'হ্যাঁ'),
        ('No', 'না'),
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

    agent = models.ForeignKey(
        'accounts.AgentInfo',
        on_delete=models.CASCADE,
        related_name='client_cvs_by_agent', blank=True, null=True
    )

    full_name = models.CharField("পূর্ণ নাম (ইংরেজি)", max_length=100, blank=True)
    full_name_bn = models.CharField("পূর্ণ নাম (বাংলা)", max_length=100, blank=True)
    phone = models.CharField("ফোন নম্বর", max_length=13, unique=True, help_text="ফোন নম্বর (যেমনঃ 01XXXXXXXXX)")

    skills = models.CharField("দক্ষতা", max_length=200, null=True, blank=True, help_text="মূল দক্ষতা")
    special_skills = models.CharField("বিশেষ দক্ষতা", max_length=200, null=True, blank=True, help_text="বিশেষ কোনো দক্ষতা থাকলে")
    bio = models.TextField("জীবনবৃত্তান্ত", blank=True, help_text="সংক্ষিপ্ত নিজের পরিচয়")

    blood_group = models.CharField("রক্তের গ্রুপ", max_length=10, choices=BLOOD_GROUP_CHOICES, default='Other')
    blood_group_other = models.CharField("অন্যান্য রক্তের গ্রুপ", max_length=20, blank=True, help_text="অন্যান্য হলে এখানে লিখুন")

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
    married = models.CharField("বৈবাহিক অবস্থা", max_length=5, choices=MARRIED_CHOICES, default='No', blank=True, null=True)

    last_education = models.CharField("সর্বশেষ শিক্ষাগত যোগ্যতা", max_length=20, choices=EDUCATION_CHOICES, default='SSC', blank=True, null=True)
    last_education_other = models.CharField("অন্যান্য শিক্ষাগত যোগ্যতা", max_length=100, blank=True, null=True, help_text="অন্যান্য হলে লিখুন")
    last_education_result = models.CharField("ফলাফল", max_length=100, blank=True, null=True)
    last_education_passing_year = models.PositiveIntegerField("পাসের বছর", blank=True, null=True)

    current_job_status = models.CharField("বর্তমান পেশার অবস্থা", max_length=20, choices=JOB_STATUS_CHOICES, default='Unemployed', blank=True, null=True)

    created_at = models.DateTimeField("তৈরির তারিখ", auto_now_add=True)
    updated_at = models.DateTimeField("আপডেটের তারিখ", auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s CV"






class PassportInfo(models.Model):
    agent = models.ForeignKey(
        'accounts.AgentInfo',
        on_delete=models.CASCADE,
        related_name='client_passports_by_agent',
        blank=True,
        null=True
    )

    profile_photo = models.ImageField(upload_to='agent/client/passport/profile/', null=True, blank=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, default='Bangladeshi', null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        null=True,
        blank=True
    )
    father_name = models.CharField(max_length=200, null=True, blank=True)
    mother_name = models.CharField(max_length=200, null=True, blank=True)
    spouse_name = models.CharField(max_length=200, blank=True, null=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    place_of_issue = models.CharField(max_length=100, null=True, blank=True)
    passport_scan_photo = models.ImageField(upload_to='agent/client/passport/scan/', null=True, blank=True)

    def __str__(self):
        if self.agent:
            return f"{self.agent.user.phone_number}'s Passport Info"
        return "Passport Info"
