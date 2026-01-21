from django.conf import settings
from django.db import models

class ClientServices(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='service_images/%Y/%m/%d/', blank=True, null=True)
    price = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        default="active",
        choices=[("active", "Active"), ("inactive", "Inactive")]
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services_created"
    )

    def __str__(self):
        return self.name if self.name else "Unnamed Service"


# class ServiceApplication(models.Model):
#     STATUS_CHOICES = [
#         ("applied", "Applied"),
#         ("pending", "Pending"),
#         ("approved", "Approved"),
#         ("rejected", "Rejected")
#     ]

#     service = models.ForeignKey('ClientServices', on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     passport_info = models.ForeignKey('form_wizard.PassportInfo', on_delete=models.CASCADE, null=True, blank=True)  # Link to PassportInfo
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
#     message = models.TextField(null=True, blank=True)
#     applied_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.phone_number} - {self.service.name} ({self.status})"

#     @property
#     def agent_info(self):
#         """
#         Retrieve the agent information linked to this passport info.
#         """
#         if self.passport_info:
#             return self.passport_info.agent  # Assuming PassportInfo has a ForeignKey to AgentInfo
#         return None


from django.utils import timezone

class ServiceApplication(models.Model):

    STATUS_CHOICES = [
        ('payment_pending', 'পেমেন্ট যাচাই চলমান'),
        ('partial_payment', 'আংশিক পেমেন্ট সম্পন্ন'),
        ('full_payment', 'পেমেন্ট পরিশোধ হয়েছে'),
        ('rejected', 'পেমেন্ট বাতিল হয়েছে'),
    ]


    service = models.ForeignKey('ClientServices', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passport_info = models.ForeignKey('form_wizard.PassportInfo', on_delete=models.CASCADE, null=True, blank=True)  # Link to PassportInfo
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="applied", verbose_name="স্ট্যাটাস", null=True, blank=True)
    message = models.TextField(null=True, blank=True, verbose_name="বার্তা")  # For application message
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="আবেদনের তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    # Payment tracking fields
    amount_paid = models.IntegerField(default=0, verbose_name="পেমেন্ট পরিমাণ")
    payment_message = models.TextField(null=True, blank=True, verbose_name="পেমেন্ট বার্তা")  # Message regarding the payment or transaction

    # Discount and discount tracking (Fixed amount)
    discount = models.IntegerField(default=0, help_text="Fixed discount amount on service price", verbose_name="ডিসকাউন্ট")
    discount_used = models.BooleanField(default=False, help_text="Indicates if discount has been used", verbose_name="ডিসকাউন্ট ব্যবহৃত")

    # Payment Due Date (new field to track due date)
    payment_due_date = models.DateField(null=True, blank=True, help_text="The date by which the full payment should be made", verbose_name="পেমেন্ট Due তারিখ")

    def __str__(self):
        return f"{self.user.phone_number} - {self.service.name} ({self.status})"

    @property
    def discounted_price(self):
        """
        Calculate the discounted price of the service.
        """
        return self.service.price - self.discount

    @property
    def balance(self):
        """
        Calculate the remaining balance for the service application dynamically.
        Apply discount if available (fixed amount).
        """
        return max(0, self.discounted_price - self.amount_paid)  # Calculate balance as the difference between discounted price and paid amount

    def save(self, *args, **kwargs):
        """
        Override save to ensure balance is recalculated each time the model is saved.
        Also update the status based on amount paid and discounted price.
        """
        # If amount_paid is greater than 0, then check if status needs to be updated
        if self.amount_paid > 0:
            if self.amount_paid < self.discounted_price:
                self.status = 'partial_payment'  # Set status to Partial Payment if paid amount is less than discounted price
            elif self.amount_paid >= self.discounted_price:
                self.status = 'full_payment'  # Set status to Full Payment if paid amount equals or exceeds discounted price
        else:
            # If amount_paid is 0, don't change the status
            self.status = 'applied'

        self.balance  # This triggers the calculation for the balance (remaining amount)
        super(ServiceApplication, self).save(*args, **kwargs)

    def add_payment(self, payment_amount, payment_message=""):
        """
        Method to add partial payment and log it.
        """
        self.amount_paid += payment_amount
        self.payment_message = payment_message
        self.save()

        # Create a log entry for this payment action
        PaymentLog.objects.create(
            service_application=self,
            amount_paid=payment_amount,
            remaining_balance=self.balance,
            payment_message=payment_message,
            action_taken="partial_payment"
        )

    def mark_full_payment(self, payment_amount, payment_message=""):
        """
        Method to mark the service application as fully paid.
        """
        self.amount_paid = self.discounted_price  # Set full payment to the discounted price
        self.payment_message = payment_message
        self.status = 'full_payment'  # Mark as full payment
        self.save()

        # Create a log entry for full payment action
        PaymentLog.objects.create(
            service_application=self,
            amount_paid=payment_amount,
            remaining_balance=0,
            payment_message=payment_message,
            action_taken="full_payment"
        )

    # def update_amount_paid(self):
    #     """
    #     Update the total amount paid in the ServiceApplication model whenever a payment is approved.
    #     """
    #     total_paid = self.clientpayment_set.filter(status="approved").aggregate(models.Sum('amount'))['amount__sum'] or 0
    #     self.amount_paid = total_paid
    #     self.save()

    def update_amount_paid(self):
        """
        Update the total amount paid in the ServiceApplication model whenever a payment is approved.
        """
        total_paid = self.client_payment_services.filter(status="approved").aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.amount_paid = total_paid
        self.save()




class ServiceApplicationProgress(models.Model):
    class Meta:
        unique_together = ('application', 'status')

    STATUS_CHOICES = [
        ("applied", "আবেদন করা হয়েছে"),
        ("payment_pending", "পেমেন্ট পেন্ডিং রয়েছে"),
        ("full_payment", "পেমেন্ট পরিষদ হয়েছে"),
        ("processing_job_permit", "জব কন্টাক্ট/ওয়ার্ক পারমিট কাজটি প্রক্রিয়াধীন"),
        ("job_permit_received", "জব কন্টাক্ট/ওয়ার্ক পারমিট রিসিভ করা হয়েছে"),
        ("visa_processing_third_country", "তৃতীয় দেশের ভিসা আবেদন প্রক্রিয়াধীন"),
        ("embassy_approval_pending", "এম্বাসি অ্যাপ্রুভ প্রক্রিয়াধীন"),
        ("visa_application_submitted", "ভিসা অ্যাপ্লিকেশন জমা দেওয়া হয়েছে"),
        ("visa_decision", "ভিসা এপ্রুভ / রিজেক্ট"),
        ("flight_date_confirmed", "ফ্লাইট বুকিং ডেট সম্পন্ন"),
    ]

    application = models.ForeignKey(
        'ServiceApplication',
        on_delete=models.CASCADE,
        related_name='progress_logs',
        verbose_name="Service Application"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='applied', verbose_name="অবস্থা")
    message = models.TextField(blank=True, null=True, verbose_name="মেসেজ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    def save_or_update_progress(application, status, message):
        """
        নির্দিষ্ট application ও status এর জন্য message update করে,
        যদি না থাকে তাহলে create করে।
        """
        obj, created = ServiceApplicationProgress.objects.update_or_create(
            application=application,
            status=status,
            defaults={'message': message}
        )
        return obj


    def __str__(self):
        return f"{self.application.user.phone_number} - {self.get_status_display()} @ {self.created_at.strftime('%d-%m-%Y')}"



class PaymentLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    service_application = models.ForeignKey(ServiceApplication, on_delete=models.CASCADE)
    amount_paid = models.IntegerField(default=0)
    remaining_balance = models.IntegerField(default=0)
    payment_message = models.TextField(null=True, blank=True)
    action_taken = models.CharField(
        max_length=255,
        choices=[('payment_pending', 'পেমেন্ট যাচাই চলমান'),
        ('partial_payment', 'আংশিক পেমেন্ট সম্পন্ন'),
        ('full_payment', 'পেমেন্ট পরিশোধ হয়েছে'),
        ('rejected', 'পেমেন্ট বাতিল হয়েছে')],
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.service_application.user.phone_number} - {self.action_taken}"


import os
import datetime

def user_upload_path(instance, filename):
    return os.path.join(
        "client", "services", "payment_receipts",
        str(instance.user.phone_number),
        datetime.datetime.now().strftime("%Y/%m/%d"),
        filename
    )



class ClientPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bkash', 'Bkash'),
        ('Rocket', 'Rocket'),
        ('Nagad', 'Nagad'),
        ('Bank', 'Bank'),
        ('Others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('pending', 'পেন্ডিং'),
        ('approved', 'অনুমোদিত'),
        ('rejected', 'বাতিল'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey('ServiceApplication', on_delete=models.CASCADE, related_name='client_payment_services')
    amount = models.IntegerField(default=0)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=user_upload_path, blank=True, null=True)

    # New Fields
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',  # Default to 'pending'
        blank=True,
        null=True
    )
    admin_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='অ্যাডমিন বার্তা'
    )

    def __str__(self):
        return f"Client: {self.user.phone_number} | Service: {self.service.service.name} | Amount: {self.amount} | Status: {self.status}"

    def save(self, *args, **kwargs):
        """
        Override save to ensure amount_paid in ServiceApplication is updated when the payment is approved.
        Also update progress status accordingly.
        """
        super(ClientPayment, self).save(*args, **kwargs)

        if self.status == 'approved':
            # Step 1: Update paid amount
            self.service.update_amount_paid()

            # Step 2: Determine status based on balance
            app = self.service  # type: ServiceApplication
            current_status = 'payment_pending'
            if app.balance == 0:
                current_status = 'full_payment'

            # Step 3: Avoid duplicate progress entries (idempotent)
            from apps.services.models import ServiceApplicationProgress  # Optional safety if circular import
            already_exists = app.progress_logs.filter(status=current_status).exists()
            if not already_exists:
                ServiceApplicationProgress.objects.create(
                    application=app,
                    status=current_status,
                    message=f"{self.admin_message or ''}".strip()
                    # message=f"Payment approved: {self.amount}৳. {self.admin_message or ''}".strip()
                )







# Notice part

class Notice(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    service = models.ForeignKey(
        ClientServices,
        on_delete=models.CASCADE,
        related_name='notices',
        blank=True,
        null=True,
        verbose_name="notice_service"
    )
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="notice_title")
    message = models.TextField(blank=True, null=True, verbose_name="notice_message")
    file = models.FileField(upload_to='notices/files/', blank=True, null=True, verbose_name="notice_file")
    image = models.ImageField(upload_to='notices/images/', blank=True, null=True, verbose_name="notice_image")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="notice_status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="notice_date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="notice_updated_date")

    def __str__(self):
        return self.title or f"Notice for {self.service.name if self.service else 'General'}"

class NoticePublic(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="notice_title")
    message = models.TextField(blank=True, null=True, verbose_name="notice_message")
    file = models.FileField(upload_to='notices_public/files/', blank=True, null=True, verbose_name="public_notice_file")
    image = models.ImageField(upload_to='notices_public/images/', blank=True, null=True, verbose_name="public_notice_image")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="notice_status_public"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="public_notice_date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="public_notice_updated_date")

    def __str__(self):
        return self.title or f"Notice for {self.service.name if self.service else 'General'}"
