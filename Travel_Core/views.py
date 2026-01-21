from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from apps.site_settings.forms import AppointmentForm
# from apps.site_settings.models import AppointmentNotice

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact-us.html')

def blogs(request):
    return render(request, 'blogs.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about-us.html')

def appointment(request):
    return render(request, 'office_appointment.html')

def video(request):
    return render(request, 'video_details.html')

def public_notices(request):
    return render (request, 'notice_details.html')

def query_form(request):
    return render(request, 'query_form.html')  # Render the form template

# def appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment_obj = form.save()
#             messages.success(request, 'আপনার অ্যাপয়েন্টমেন্ট সফলভাবে বুক হয়েছে! আমরা শীঘ্রই আপনার সাথে যোগাযোগ করব।')
#             return redirect('appointment')
#         else:
#             messages.error(request, 'দয়া করে সকল তথ্য সঠিকভাবে পূরণ করুন।')
#     else:
#         form = AppointmentForm()

#     # Get active notices
#     notices = AppointmentNotice.objects.filter(is_active=True)

#     context = {
#         'form': form,
#         'notices': notices,
#     }
#     return render(request, 'office_appointment.html', context)
