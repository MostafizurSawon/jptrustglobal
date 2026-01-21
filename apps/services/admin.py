from django.contrib import admin
from .models import ClientServices,ServiceApplication, PaymentLog,ServiceApplicationProgress, ClientPayment, Notice, NoticePublic

# Register your models here.
admin.site.register(ClientServices)

class ServiceApplicationAdmin(admin.ModelAdmin):
    list_display = ['service', 'user', 'status', 'amount_paid', 'balance', 'applied_at', 'updated_at']
    search_fields = ['user__phone_number', 'service__name']

class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ['service_application', 'amount_paid', 'remaining_balance', 'action_taken', 'created_at']
    search_fields = ['service_application__user__phone_number']

admin.site.register(ServiceApplication, ServiceApplicationAdmin)
admin.site.register(PaymentLog, PaymentLogAdmin)

admin.site.register(ClientPayment)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['service', 'message', 'created_at']
    search_fields = ['message', 'service__name']

admin.site.register(Notice, NoticeAdmin)
admin.site.register(ServiceApplicationProgress)
admin.site.register(NoticePublic)
