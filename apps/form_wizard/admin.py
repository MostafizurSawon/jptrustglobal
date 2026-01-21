from django.contrib import admin
from . models import TravelAgencyCV,GuestCV,Language,PassportInfo
# Register your models here.
# admin.site.register(TravelAgencyCV)
admin.site.register(GuestCV)
admin.site.register(Language)
admin.site.register(PassportInfo)
