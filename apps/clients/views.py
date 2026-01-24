
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from apps.form_wizard.models import GuestCV, PassportInfo
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib import messages

def admin_role_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            messages.error(request, "You are not authorized to access this page.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@method_decorator(admin_role_required, name='dispatch')
class AllGuestCvView(View):
    template_name = 'guest_cv_list.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        guest_cvs = GuestCV.objects.all()

        if search_query:
            guest_cvs = guest_cvs.filter(
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(user__phone_number__icontains=search_query) |
                Q(current_job_status__icontains=search_query) |
                Q(skills__icontains=search_query)
            )

        paginator = Paginator(guest_cvs, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = TemplateLayout.init(self, {
            'guest_cvs': page_obj,
            'search_query': search_query
        })

        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        return render(request, self.template_name, context)


@method_decorator(admin_role_required, name='dispatch')
class DeleteGuestCvView(View):
    def post(self, request, pk):
        cv = get_object_or_404(GuestCV, pk=pk)
        cv.delete()
        messages.success(request, "CV deleted successfully.")
        return redirect('guest_cv_list')



# Clients cv all

from django.core.paginator import Paginator
from django.db.models import Q

@method_decorator(admin_role_required, name='dispatch')
class AllClientCvView(View):
    template_name = 'client/client_cv_list.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('search', '').strip()
        guest_cvs = GuestCV.objects.all()

        # ✅ Apply search filter across relevant fields
        if query:
            guest_cvs = guest_cvs.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) |
                Q(designation__icontains=query)
                # Add more Q fields if needed from GuestCV
            )

        # ✅ Apply pagination (25 per page)
        paginator = Paginator(guest_cvs, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = TemplateLayout.init(self, {
            'guest_cvs': page_obj,
            'search_query': query,
        })

        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        return render(request, self.template_name, context)

@method_decorator(admin_role_required, name='dispatch')
class ClientCVDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        cv = get_object_or_404(GuestCV, pk=pk)
        cv.delete()
        messages.success(request, "CV deleted successfully.")
        return redirect('client_cv_list')


# Clients Passport All


@method_decorator(admin_role_required, name='dispatch')
class AllClientPassportView(View):
    template_name = 'client/client_passport_list.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('search', '').strip()
        passports = PassportInfo.objects.all()

        if query:
            passports = passports.filter(
                Q(name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(passport_number__icontains=query) |
                Q(nid__icontains=query)
                # Add more searchable fields as needed
            )

        paginator = Paginator(passports, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = TemplateLayout.init(self, {
            'passports': page_obj,
            'search_query': query,
        })
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")
        return render(request, self.template_name, context)



from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.form_wizard.forms import PassportInfoForm
from apps.form_wizard.models import PassportInfo
from web_project import TemplateLayout, TemplateHelper


@method_decorator(admin_role_required, name='dispatch')
class PassportInfoEditAdminView(LoginRequiredMixin, UpdateView):
    model = PassportInfo
    form_class = PassportInfoForm
    template_name = 'admin/passport_edit_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass user to form if needed
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "পাসপোর্ট তথ্য সম্পাদনা"
        return context

    def form_valid(self, form):
        messages.success(self.request, "পাসপোর্ট তথ্য সফলভাবে আপডেট করা হয়েছে।")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "পাসপোর্ট তথ্য আপডেট করতে ব্যর্থ হয়েছে। দয়া করে ফর্মটি যাচাই করুন।")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('client_passport_list')





@method_decorator(admin_role_required, name='dispatch')
class PassportDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        passport = get_object_or_404(PassportInfo, pk=pk)
        passport.delete()
        messages.success(request, "পাসপোর্ট তথ্য সফলভাবে মুছে ফেলা হয়েছে।")
        return redirect('client_passport_list')




#  experiment
from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.form_wizard.models import PassportInfo
from django.contrib.auth import get_user_model
from web_project import TemplateLayout

User = get_user_model()

class PassportInfoByUserView(View):
    template_name = 'client/passport_info_by_user.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        passport = get_object_or_404(PassportInfo, user=user)



        context = TemplateLayout.init(self, {
            'user': user,
            'passport': passport
        })
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")
        return render(request, self.template_name, context)





class PassportInfoDetailView(View):
    template_name = 'client/client_passport_list.html'

    def get(self, request, *args, **kwargs):
        # Get the PassportInfo object by ID
        passport_info = get_object_or_404(PassportInfo, id=kwargs['pk'])

        context = TemplateLayout.init(self, {'passport_info': passport_info})

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # Return the response containing the modal with passport info
        return render(request, self.template_name, context)


from apps.form_wizard.forms import PassportInfoForm
from django.http import JsonResponse

class PassportInfoEditView(View):
    template_name = 'client/client_passport_list.html'

    def get(self, request, *args, **kwargs):
        passport_info = get_object_or_404(PassportInfo, id=kwargs['pk'])
        form = PassportInfoForm(instance=passport_info)
        context = TemplateLayout.init(self, {
            'form': form,
            'passport_info': passport_info,
        })

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")



        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        passport_info = get_object_or_404(PassportInfo, id=kwargs['pk'])
        form = PassportInfoForm(request.POST, request.FILES, instance=passport_info)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Passport Info updated successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})




class GuestCVDetailView(View):
    template_name = 'guest_cv_detail_admin.html'

    def get(self, request, pk, *args, **kwargs):
        guest_cv = get_object_or_404(GuestCV, pk=pk)

        # Initialize the context with TemplateLayout
        context = TemplateLayout.init(self, {'cv': guest_cv})

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        return render(request, self.template_name, context)

class GuestCVDetailView2(View):
    template_name = 'guest_cv_detail_admin2.html'

    def get(self, request, pk, *args, **kwargs):
        guest_cv = get_object_or_404(GuestCV, pk=pk)

        # Initialize the context with TemplateLayout
        context = TemplateLayout.init(self, {'cv': guest_cv})

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        return render(request, self.template_name, context)


from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.form_wizard.models import GuestCV
from apps.form_wizard.forms import TravelAgencyCVForm
from django.contrib import messages
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

class GuestCVEditView(View):
    template_name = 'guest_cv_edit.html'

    def get(self, request, pk, *args, **kwargs):
        guest_cv = get_object_or_404(GuestCV, pk=pk)
        form = TravelAgencyCVForm(instance=guest_cv)

        context = TemplateLayout.init(self, {'form': form, 'guest_cv': guest_cv})
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        guest_cv = get_object_or_404(GuestCV, pk=pk)
        form = TravelAgencyCVForm(request.POST, request.FILES, instance=guest_cv)

        if form.is_valid():
            form.save()
            messages.success(request, "CV updated successfully.")
            return redirect('guest_cv_detail', pk=pk)
        else:
            messages.error(request, "Please correct the errors below.")
            context = TemplateLayout.init(self, {'form': form, 'guest_cv': guest_cv})
            context["layout_path"] = context.get("layout_path", "layout_vertical.html")
            return render(request, self.template_name, context)






# Client Payment Information


from django.views.generic import ListView
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from apps.services.models import ClientPayment, ClientServices
from web_project import TemplateLayout, TemplateHelper


class ClientPaymentListView(ListView):
    model = ClientPayment
    template_name = 'client/client_payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = ClientPayment.objects.filter(user=user).select_related('service', 'service__service')

        service_name = self.request.GET.get('service_name')
        search_query = self.request.GET.get('search')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if service_name:
            qs = qs.filter(service__service__name=service_name)

        if search_query:
            qs = qs.filter(
                Q(transaction_id__icontains=search_query) |
                Q(message__icontains=search_query) |
                Q(admin_message__icontains=search_query)
            )

        if start_date:
            try:
                qs = qs.filter(payment_date__date__gte=start_date)
            except:
                pass

        if end_date:
            try:
                qs = qs.filter(payment_date__date__lte=end_date)
            except:
                pass

        return qs.order_by('-payment_date')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_services = ClientPayment.objects.filter(user=self.request.user).values('service__service__name').distinct()
        service_names = [s['service__service__name'] for s in user_services]
        services = ClientServices.objects.filter(name__in=service_names)

        # total_paid = sum(app.amount_paid for app in user_services)
        # total_due = sum(app.balance for app in user_services)
        # context['total_paid'] = total_paid
        # context['total_due'] = total_due

        context['services'] = services
        context['service_filter'] = self.request.GET.get('service_name', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')

        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context




# invoice
from django.shortcuts import get_object_or_404
from django.views.generic import View
from apps.services.models import ClientPayment
from web_project import TemplateLayout, TemplateHelper  # Assuming these are imported from your project

class PaymentInvoiceView(View):
    template_name = 'client/payment_invoice.html'  # Define the template for invoice

    def get(self, request, payment_id):
        # Get the payment object based on the payment_id
        payment = get_object_or_404(ClientPayment, id=payment_id)

        # Generate the invoice context
        context = {
            'payment': payment,  # The ClientPayment object
            'service': payment.service,  # The related service object
        }
        context['section_list'] = [
            ('ক্লায়েন্ট কপি', 'danger-subtle', 'bg_paid'),
            ('অফিস কপি', 'primary-subtle', 'bg_paid'),
        ]


        # Initialize context with layout settings, similar to how it's done in ClientPaymentListView
        context = TemplateLayout.init(self, context)
        context["layout"] = "vertical"
        context['show_print'] = True
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        # Return the invoice template with the payment details
        return render(request, self.template_name, context)








# details

from django.views.generic import DetailView

class ClientPaymentDetailView(DetailView):
    model = ClientPayment
    template_name = 'client/client_payment_detail.html'
    context_object_name = 'payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add layout context if needed (using TemplateLayout.init() or your custom layout)
        context["layout"] = "vertical"
        context['show_print'] = True
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context




# invoice verification
from django.shortcuts import render
from django.views import View
from apps.services.models import ClientPayment
from web_project import TemplateLayout, TemplateHelper

class PaymentInvoiceSearchView(View):
    template_name = 'client/invoice_search.html'

    def get(self, request):
        context = TemplateLayout.init(self, {})
        payment_id = request.GET.get('payment_id')

        if payment_id:
            try:
                payment = ClientPayment.objects.select_related('service__service').get(id=payment_id)
                context['payment'] = payment
            except ClientPayment.DoesNotExist:
                context['error'] = True
                context['searched_id'] = payment_id

        context["layout_path"] = TemplateHelper.set_layout("layout_blank.html", context)
        return render(request, self.template_name, context)

    def post(self, request):
        context = TemplateLayout.init(self, {})
        payment_id = request.POST.get('payment_id')

        try:
            payment = ClientPayment.objects.select_related('service__service').get(id=payment_id)
            context['payment'] = payment
        except ClientPayment.DoesNotExist:
            context['error'] = True
            context['searched_id'] = payment_id

        context["layout_path"] = TemplateHelper.set_layout("layout_blank.html", context)
        return render(request, self.template_name, context)



# Application Status
# from django.views.generic import ListView
# from apps.services.models import ServiceApplication, ClientPayment

# # Timeline step definitions
# TIMELINE_STEPS = [
#     ("applied", "আবেদন করা হয়েছে", "আপনার আবেদন সফলভাবে জমা দেওয়া হয়েছে।"),
#     ("payment_pending", "পেমেন্ট পেন্ডিং রয়েছে", "পেমেন্ট এখনও সম্পন্ন হয়নি। অনুগ্রহ করে পেমেন্ট করুন।"),
#     ("full_payment", "পেমেন্ট পরিষদ হয়েছে", "আপনার পেমেন্ট সম্পন্ন হয়েছে। পরবর্তী ধাপে প্রক্রিয়া চলবে।"),
#     ("processing_job_permit", "জব কন্টাক্ট/ওয়ার্ক পারমিট প্রক্রিয়াধীন", "ওয়ার্ক পারমিট/জব কন্টাক্ট প্রক্রিয়াধীন রয়েছে।"),
#     ("job_permit_received", "জব কন্টাক্ট/ওয়ার্ক পারমিট রিসিভ", "জব কন্টাক্ট/ওয়ার্ক পারমিট রিসিভ করা হয়েছে।"),
#     ("visa_processing_third_country", "তৃতীয় দেশের ভিসা প্রক্রিয়া", "তৃতীয় দেশের ভিসা আবেদন প্রক্রিয়াধীন রয়েছে।"),
#     ("embassy_approval_pending", "এম্বাসি অ্যাপ্রুভ প্রক্রিয়া", "আপনার আবেদন এখন এম্বাসির অনুমোদনের অপেক্ষায়।"),
#     ("visa_application_submitted", "ভিসা অ্যাপ্লিকেশন জমা", "আপনার ভিসা আবেদন জমা দেওয়া হয়েছে।"),
#     ("visa_decision", "ভিসা এপ্রুভ / রিজেক্ট", "আপনার ভিসার চূড়ান্ত সিদ্ধান্ত পাওয়া গেছে।"),
#     ("flight_date_confirmed", "ফ্লাইট বুকিং সম্পন্ন", "আপনার ফ্লাইট বুকিং নিশ্চিত করা হয়েছে। শুভ যাত্রা!"),
# ]

# # Timeline progress mapping
# STATUS_PROGRESS = {
#     "applied": 5,
#     "payment_pending": 15,
#     "full_payment": 25,
#     "processing_job_permit": 40,
#     "job_permit_received": 50,
#     "visa_processing_third_country": 60,
#     "embassy_approval_pending": 70,
#     "visa_application_submitted": 80,
#     "visa_decision": 90,
#     "flight_date_confirmed": 100,
# }


# class ApplicationStatusListView(ListView):
#     model = ServiceApplication
#     template_name = 'client/application_status_list.html'
#     context_object_name = 'applications'

#     def get_queryset(self):
#         queryset = ServiceApplication.objects.filter(user=self.request.user)

#         service_name = self.request.GET.get('service_name')
#         if service_name:
#             queryset = queryset.filter(service__name=service_name)

#         for app in queryset:
#             # Progress value
#             app.progress = STATUS_PROGRESS.get(app.status, 0)

#             # Timeline steps
#             app.timeline_status = []
#             current_status_found = False
#             for code, label, description in TIMELINE_STEPS:
#                 is_current = code == app.status
#                 app.timeline_status.append({
#                     "code": code,
#                     "label": label,
#                     "description": description,
#                     "active": not current_status_found,
#                     "current": is_current,
#                 })
#                 if is_current:
#                     current_status_found = True

#             # Latest approved payment info
#             latest_payment = app.client_payment_services.filter(status="approved").last()
#             if latest_payment:
#                 app.latest_admin_message = latest_payment.admin_message
#                 app.latest_payment_date = latest_payment.payment_date
#                 app.latest_payment_amount = latest_payment.amount
#             else:
#                 app.latest_admin_message = None
#                 app.latest_payment_date = None
#                 app.latest_payment_amount = None

#         return queryset

#     def get_context_data(self, **kwargs):
#         queryset = self.get_queryset()
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         context['applications'] = queryset

#         # Totals
#         total_paid = sum(app.amount_paid for app in queryset)
#         total_due = sum(app.balance for app in queryset)

#         # Distinct services for filter
#         user_services = ServiceApplication.objects.filter(user=self.request.user).values('service__name').distinct()
#         service_names = [s['service__name'] for s in user_services]

#         context.update({
#             'services': service_names,
#             'total_paid': total_paid,
#             'total_due': total_due,
#             "layout": "vertical",
#             "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
#         })
#         return context



from django.views.generic import ListView
from apps.services.models import ServiceApplication, ClientPayment, ServiceApplicationProgress
from django.db.models import Max

# Timeline definitions
# TIMELINE_STEPS = [
#     ("applied", "আবেদন করা হয়েছে", "আপনার আবেদন সফলভাবে জমা দেওয়া হয়েছে।"),
#     ("payment_pending", "পেমেন্ট পেন্ডিং রয়েছে", "পেমেন্ট এখনও সম্পন্ন হয়নি। অনুগ্রহ করে পেমেন্ট করুন।"),
#     ("full_payment", "পেমেন্ট পরিষদ হয়েছে", "আপনার পেমেন্ট সম্পন্ন হয়েছে। পরবর্তী ধাপে প্রক্রিয়া চলবে।"),
#     ("processing_job_permit", "জব কন্টাক্ট/ওয়ার্ক পারমিট প্রক্রিয়াধীন", "ওয়ার্ক পারমিট/জব কন্টাক্ট প্রক্রিয়াধীন রয়েছে।"),
#     ("job_permit_received", "জব কন্টাক্ট/ওয়ার্ক পারমিট রিসিভ", "জব কন্টাক্ট/ওয়ার্ক পারমিট রিসিভ করা হয়েছে।"),
#     ("visa_processing_third_country", "তৃতীয় দেশের ভিসা প্রক্রিয়া", "তৃতীয় দেশের ভিসা আবেদন প্রক্রিয়াধীন রয়েছে।"),
#     ("embassy_approval_pending", "এম্বাসি অ্যাপ্রুভ প্রক্রিয়া", "আপনার আবেদন এখন এম্বাসির অনুমোদনের অপেক্ষায়।"),
#     ("visa_application_submitted", "ভিসা অ্যাপ্লিকেশন জমা", "আপনার ভিসা আবেদন জমা দেওয়া হয়েছে।"),
#     ("visa_decision", "ভিসা এপ্রুভ / রিজেক্ট", "আপনার ভিসার চূড়ান্ত সিদ্ধান্ত পাওয়া গেছে।"),
#     ("flight_date_confirmed", "ফ্লাইট বুকিং সম্পন্ন", "আপনার ফ্লাইট বুকিং নিশ্চিত করা হয়েছে। শুভ যাত্রা!"),
# ]
TIMELINE_STEPS = [
    ("applied", "Applied", "Your application has been successfully submitted."),
    ("payment_pending", "Payment Pending", "Payment is still pending. Please make the payment."),
    ("full_payment", "Paid", "Your payment has been completed. The process will continue to the next step."),
    (
        "processing_job_permit",
        "Job: Job Contract / Work Permit Processing\n"
        "Study: Admission Test / Interview Stage\n"
        "Visit: Invitation & Supporting Documents in Progress",
        "Your application is currently being processed."
    ),
    (
        "job_permit_received",
        "Job: Job Contract / Work Permit Received\n"
        "Study: Admission Result / Offer Letter Received\n"
        "Visit: All Documentation Completed",
        ""
    ),
    (
        "visa_processing_third_country",
        "Third Country Visa Application",
        "Your visa application for the third country is under process."
    ),
    (
        "embassy_approval_pending",
        "Embassy Appointment & Documentation Pending",
        ""
    ),
    (
        "visa_application_submitted",
        "Visa Application Submitted",
        "Your visa application has been submitted successfully."
    ),
    (
        "visa_decision",
        "Visa Decision (Approved / Rejected)",
        "The final decision on your visa has been received."
    ),
    (
        "flight_date_confirmed",
        "Flight Booking Confirmed",
        "Your flight has been successfully booked. Have a safe and wonderful journey!"
    ),
]

# Status → Progress %
STATUS_PROGRESS = {
    "applied": 5,
    "payment_pending": 15,
    "full_payment": 25,
    "processing_job_permit": 40,
    "job_permit_received": 50,
    "visa_processing_third_country": 60,
    "embassy_approval_pending": 70,
    "visa_application_submitted": 80,
    "visa_decision": 90,
    "flight_date_confirmed": 100,
}


class ApplicationStatusListView(ListView):
    model = ServiceApplication
    template_name = 'client/application_status_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = ServiceApplication.objects.filter(user=self.request.user)\
            .select_related('service')\
            .prefetch_related('progress_logs', 'client_payment_services')

        service_name = self.request.GET.get('service_name')
        if service_name:
            queryset = queryset.filter(service__name=service_name)

        for app in queryset:
            # Get latest progress log
            # latest_progress = app.progress_logs.order_by('-created_at').first()
            latest_progress = app.progress_logs.order_by('-updated_at').first()
            current_status = latest_progress.status if latest_progress else "applied"
            app.current_status = current_status
            app.progress = STATUS_PROGRESS.get(current_status, 0)

            # Build timeline with matched logs
            logs_by_status = {log.status: log for log in app.progress_logs.all()}
            app.timeline_status = []
            for code, label, description in TIMELINE_STEPS:
                log = logs_by_status.get(code)
                index = [s[0] for s in TIMELINE_STEPS].index(code)
                current_index = [s[0] for s in TIMELINE_STEPS].index(current_status)

                app.timeline_status.append({
                    "code": code,
                    "label": label,
                    "description": description,
                    "active": log is not None,
                    "current": code == current_status,
                    "message": log.message if log else None,
                    "past": index < current_index  # ✅ নতুন ফ্ল্যাগ
                })


            # Latest approved payment info
            latest_payment = app.client_payment_services.filter(status="approved").last()
            app.latest_admin_message = getattr(latest_payment, 'admin_message', None)
            app.latest_payment_date = getattr(latest_payment, 'payment_date', None)
            app.latest_payment_amount = getattr(latest_payment, 'amount', None)

        return queryset

    def get_context_data(self, **kwargs):
        applications = self.get_queryset()
        context = TemplateLayout.init(self, {'applications': applications})

        total_paid = sum(app.amount_paid for app in applications)
        total_due = sum(app.balance for app in applications)


        services = ServiceApplication.objects.filter(user=self.request.user)\
            .values_list('service__name', flat=True).distinct()

        context.update({
            'applications': applications,
            'services': services,
            'total_paid': total_paid,
            'total_due': total_due,
            "layout": "vertical",
            "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        })
        return context




# Customer Support
from django.views.generic import ListView
from django.db.models import Q
from .models import CustomerSupport

class CustomerSupportListView(ListView):
    model = CustomerSupport
    template_name = 'support/support_list.html'
    context_object_name = 'supports'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = CustomerSupport.objects.filter(user=user)

        search_query = self.request.GET.get('search')
        status_filter = self.request.GET.get('status')

        if search_query:
            qs = qs.filter(message__icontains=search_query)

        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import CustomerSupport
from .forms import CustomerSupportForm
from web_project import TemplateLayout, TemplateHelper

class CustomerSupportCreateView(CreateView):
    model = CustomerSupport
    form_class = CustomerSupportForm
    template_name = 'support/support_form.html'
    success_url = reverse_lazy('support_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "সাপোর্ট রিকুয়েস্ট সফলভাবে জমা দেওয়া হয়েছে।")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout'] = "vertical"
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context



# Chat Details
from django.views.generic import DetailView
from .models import CustomerSupport, CustomerSupportReply
from web_project import TemplateLayout, TemplateHelper

class CustomerSupportDetailView(DetailView):
    model = CustomerSupport
    template_name = 'support/support_detail.html'
    context_object_name = 'support'

    def get_queryset(self):
        # Ensure only the owner can view
        return CustomerSupport.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout'] = "vertical"
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context






class SupportChatView(View):
    def get(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk, user=request.user)

        # 🔻 Mark as read for user
        if support.user_unread:
            support.user_unread = False
            support.save(update_fields=['user_unread'])

        if support.status != 'in_progress':
            messages.error(request, "এই টিকিটে এখন চ্যাট করা যাবে না।")
            return redirect('support_list')


        replies = support.replies.select_related('sender').order_by('created_at')

        context = TemplateLayout.init(self, {
            'support': support,
            'replies': replies,
        })
        context['layout'] = "vertical"
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)

        return render(request, 'support/support_chat.html', context)



    def post(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk, user=request.user)
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        if support.status != 'in_progress':
            messages.error(request, "এই টিকিটে এখন চ্যাট করা যাবে না।")
            return redirect('support_list')


        if message or attachment:
            CustomerSupportReply.objects.create(
                support=support,
                sender=request.user,
                message=message,
                attachment=attachment
            )
            support.status = 'in_progress'
            support.admin_unread = True  # mark for admin
            support.save()


        return redirect('support_chat', pk=pk)


# Admin Part


@method_decorator(admin_role_required, name='dispatch')
class AdminSupportListView(ListView):
    model = CustomerSupport
    template_name = 'support/admin_support_list.html'
    context_object_name = 'supports'
    paginate_by = 20

    def get_queryset(self):
        qs = CustomerSupport.objects.all().select_related('user')
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')

        if search:
            qs = qs.filter(
                Q(user__username__icontains=search) |
                Q(user__phone_number__icontains=search) |
                Q(message__icontains=search)
            )

        if status:
            qs = qs.filter(status=status)

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context

from django.http import HttpResponseRedirect
from django.urls import reverse

@method_decorator(admin_role_required, name='dispatch')
class AdminSupportDeleteView(View):
    def post(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk)
        support.delete()
        messages.success(request, "সাপোর্ট টিকিট সফলভাবে মুছে ফেলা হয়েছে।")
        return HttpResponseRedirect(reverse('admin_support_list'))


# status update

def update_status(request, pk, status):
    support = get_object_or_404(CustomerSupport, pk=pk)
    if request.user.is_staff:
        support.status = status
        support.save()
    return redirect('admin_support_chat', pk=pk)




@method_decorator(admin_role_required, name='dispatch')
class AdminSupportChatView(View):
    def get(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk)

        # 🔻 Mark as read for admin
        if support.admin_unread:
            support.admin_unread = False
            support.save(update_fields=['admin_unread'])

        replies = support.replies.select_related('sender').order_by('created_at')

        context = TemplateLayout.init(self, {
            'support': support,
            'replies': replies,
        })
        context['layout'] = "vertical"
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)

        return render(request, 'support/admin_support_chat.html', context)

    def post(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk)
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        if message or attachment:
            CustomerSupportReply.objects.create(
                support=support,
                sender=request.user,
                message=message,
                attachment=attachment
            )
            support.status = 'in_progress'
            support.user_unread = True  # mark for user
            support.save()

        return redirect('admin_support_chat', pk=pk)





# edit
from django.http import JsonResponse
from .forms import CustomerSupportAdminForm

@method_decorator(admin_role_required, name='dispatch')
class AdminSupportEditView(View):
    def get(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk)
        form = CustomerSupportAdminForm(instance=support)
        context = {
            'form': form,
            'support': support
        }
        return render(request, 'support/support_edit_form.html', context)

    def post(self, request, pk):
        support = get_object_or_404(CustomerSupport, pk=pk)
        form = CustomerSupportAdminForm(request.POST, instance=support)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('support/support_edit_form.html', {'form': form, 'support': support}, request)
            return JsonResponse({'success': False, 'html': html})
