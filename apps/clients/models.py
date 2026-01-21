from django.db import models

class Transaction(models.Model):
    customer = models.CharField(max_length=150)
    transaction_date = models.DateField()
    due_date = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Due", "Due"), ("Canceled", "Canceled")])

    def __str__(self):
        return self.customer



from django.conf import settings

class CustomerSupport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_requests')
    message = models.TextField(verbose_name='Customer Message')
    reply = models.TextField(verbose_name='Admin Reply', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_unread = models.BooleanField(default=False, null=True, blank=True)
    user_unread = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Support from {self.user.phone_number if hasattr(self.user, 'phone_number') else self.user.username} - {self.status}"




class CustomerSupportReply(models.Model):
    support = models.ForeignKey('CustomerSupport', on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='support/support_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_admin(self):
        return self.sender.is_staff  # Adjust if using roles
