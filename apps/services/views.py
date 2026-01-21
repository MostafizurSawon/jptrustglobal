from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import ClientServices
from .forms import ClientServicesForm
from web_project import TemplateLayout, TemplateHelper
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

# class ClientServiceCreateView(LoginRequiredMixin, CreateView):
#     model = ClientServices
#     form_class = ClientServicesForm
#     template_name = 'create_service.html'

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.created_by = self.request.user
#         instance.save()
#         messages.success(self.request, "Service created successfully.")
#         return redirect('create_service')  # Update this to the actual target page

#     def form_invalid(self, form):
#         messages.error(self.request, "Please correct the errors below.")
#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
#         context["services"] = ClientServices.objects.all()
#         return context

from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

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
class ClientServiceListView(LoginRequiredMixin, CreateView):
    model = ClientServices
    form_class = ClientServicesForm
    template_name = 'create_service.html'

    def post(self, request, *args, **kwargs):
        service_id = request.POST.get('service_id')
        if service_id:
            service = get_object_or_404(ClientServices, id=service_id)
            form = self.form_class(request.POST, request.FILES, instance=service)
            action = "updated"
        else:
            form = self.form_class(request.POST, request.FILES)
            action = "created"

        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            messages.success(request, f"Service {action} successfully.")
            return redirect('client_services_list')
        else:
            messages.error(request, "Please correct the errors below.")
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["services"] = ClientServices.objects.all()
        return context


@method_decorator(admin_role_required, name='dispatch')
class ClientServiceDetailView(DetailView):
    model = ClientServices
    template_name = 'service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context

@method_decorator(admin_role_required, name='dispatch')
class ClientServiceDeleteView(DeleteView):
    model = ClientServices
    success_url = reverse_lazy('client_services_list')
    template_name = 'service_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context

    def delete(self, request, *args, **kwargs):
        messages.danger(request, "Service deleted successfully.")
        return super().delete(request, *args, **kwargs)



# guest / client section

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from apps.form_wizard.models import PassportInfo
from .models import ServiceApplication, ClientServices
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

class ServiceApplyView(View):
    template_name = 'client_service_list.html'

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        # Check if the user has passport info and pass it to the context
        has_passport_info = hasattr(request.user, 'passport_info')

        if request.user.role == 'guest' and not has_passport_info:
            print(request.user.role, "User is a guest, redirecting to passport info creation.")
            # If the user does not have passport info, redirect to the create passport page
            messages.error(request, "আবেদন করার জন্য প্রথমে আপনার পাসপোর্ট তথ্য তৈরি করুন!")

        # Get all services to display
        services = ClientServices.objects.filter(status='active')


        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            services = services.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        # Pagination
        paginator = Paginator(services, 9)  # 6 services per page
        page_number = request.GET.get('page')
        services_page = paginator.get_page(page_number)

        # Create a dictionary to store whether the user has already applied for each service
        applied_services = ServiceApplication.objects.filter(user=request.user).values_list('service', flat=True)

        context["services"] = services_page
        context["applied_services"] = applied_services  # A list of service IDs the user has applied for
        context["has_passport_info"] = has_passport_info  # Pass the passport info status to the context
        context["search_query"] = search_query  # Pass the search query to the context for re-rendering

        # Pagination variables
        context["paginator"] = paginator
        context["services_page"] = services_page
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        service_id = request.POST.get('service_id')
        message = request.POST.get('message')

        # Check if the user has passport info before proceeding with the service application
        if request.user.role == 'guest':
            if not hasattr(request.user, 'passport_info'):
                messages.error(request, "আবেদন করার জন্য প্রথমে আপনার পাসপোর্ট তথ্য তৈরি করুন!")
                return redirect('passport_info_create')  # Redirect to the passport info creation page

        if service_id and message:
            try:
                # Fetch the selected service
                service = ClientServices.objects.get(id=service_id)
                user = request.user
                passport_info = request.user.passport_info  # Get the user's passport_info

                # Check if the user has already applied for this service
                if ServiceApplication.objects.filter(user=user, service=service).exists():
                    messages.error(request, f"আপনি ইতিমধ্যেই {service.name} সেবার জন্য আবেদন করেছেন।")
                    return redirect('service_apply')  # Redirect back to the service application page

                # Create a new service application and link it to the passport_info
                service_application = ServiceApplication.objects.create(
                    service=service,
                    user=user,
                    passport_info=passport_info,  # Associate the passport info with the service application
                    status='applied',
                )

                # Save the message if provided
                service_application.message = message
                service_application.save()

                # Success message
                messages.success(request, f"{service.name} সেবার জন্য আপনার আবেদন গ্রহণ করা হয়েছে। আমরা শীঘ্রই আপনার সাথে যোগাযোগ করব!")
                return redirect('applied_service_apply')  # Redirect back to the service application page or success page
            except ClientServices.DoesNotExist:
                messages.error(request, "নির্বাচিত সেবা পাওয়া যায়নি।")
                return redirect('service_apply')

        messages.error(request, "ত্রুটি! অনুগ্রহ করে সেবা এবং বার্তা প্রদান করুন।")
        return redirect('service_apply')




# My Service Application View From dashboard Directly

# class ServiceApplyViewDashboard(View):
#     template_name = 'client_service_list.html'

#     def get(self, request, *args, **kwargs):
#         context = TemplateLayout.init(self, {})
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         # Check if the user has a PassportInfo instance
#         if not hasattr(request.user, 'passport_info'):
#             # If not, redirect to the create passport page
#             return redirect('passport_info_create')  # Assuming 'passport_info_create' is the URL name for creating a passport

#         # Get all services to display
#         services = ClientServices.objects.all()

#         # Create a dictionary to store whether the user has already applied for each service
#         applied_services = ServiceApplication.objects.filter(user=request.user).values_list('service', flat=True)

#         # Pass this information to the context
#         context["services"] = services
#         context["applied_services"] = applied_services  # A list of service IDs the user has applied for
#         return render(request, self.template_name, context)

#     @method_decorator(login_required)  # Ensure the user is logged in
#     def post(self, request, *args, **kwargs):
#         # Check if the user has a PassportInfo instance
#         if not hasattr(request.user, 'passport_info'):
#             # If not, redirect to create passport page
#             messages.error(request, "You need to create your passport info first!")
#             return redirect('passport_info_create')  # Redirect to the passport info creation page

#         service_id = request.POST.get('service_id')
#         message = request.POST.get('message')

#         if service_id and message:
#             try:
#                 # Fetch the selected service
#                 service = ClientServices.objects.get(id=service_id)
#                 user = request.user
#                 passport_info = request.user.passport_info  # Get the user's passport_info

#                 # Check if the user has already applied for this service
#                 if ServiceApplication.objects.filter(user=user, service=service).exists():
#                     messages.error(request, f"You have already applied for the service: {service.name}.")
#                     return redirect('service_apply')  # Redirect back to the service application page

#                 # Create a new service application and link it to the passport_info
#                 service_application = ServiceApplication.objects.create(
#                     service=service,
#                     user=user,
#                     passport_info=passport_info,  # Associate the passport info with the service application
#                     status='applied',
#                 )

#                 # Save the message if provided
#                 service_application.message = message
#                 service_application.save()

#                 # Success message
#                 messages.success(request, f"Thank you for applying for {service.name}. We will get back to you shortly!")
#                 return redirect('service_apply')  # Redirect back to the service application page or success page
#             except ClientServices.DoesNotExist:
#                 messages.error(request, "Selected service not found.")
#                 return redirect('service_apply')

#         messages.error(request, "Error! Please provide a service and message.")
#         return redirect('service_apply')


from django.views.generic import ListView
from django.db.models import Q
from .models import ServiceApplication
from web_project import TemplateLayout, TemplateHelper

class MyServiceApplyView(ListView):
    model = ServiceApplication
    template_name = 'client/my_service_application_list.html'
    context_object_name = 'service_applications'
    paginate_by = 10  # Enable pagination

    def get_queryset(self):
        queryset = ServiceApplication.objects.filter(user=self.request.user)

        # Filtering
        self.service_name = self.request.GET.get('service_name')
        self.search_query = self.request.GET.get('search')

        if self.service_name:
            queryset = queryset.filter(service__name=self.service_name)

        if self.search_query:
            queryset = queryset.filter(
                Q(service__name__icontains=self.search_query) |
                Q(message__icontains=self.search_query)
            )

        # Save filtered queryset to use in context
        self.filtered_queryset = queryset
        return queryset.order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        # Distinct service names for dropdown filter
        service_names = ServiceApplication.objects.filter(user=self.request.user).values_list('service__name', flat=True).distinct()
        context['services'] = service_names

        # Calculate totals using filtered queryset
        applications = self.filtered_queryset

        total_paid = sum(app.amount_paid for app in applications)
        total_due = sum(app.balance for app in applications)

        context['total_paid'] = total_paid
        context['total_due'] = total_due

        return context







#  Admin Section
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib import messages
from django.http import JsonResponse
from .models import ServiceApplication, ServiceApplicationProgress
from web_project import TemplateLayout, TemplateHelper
import json

@method_decorator(admin_role_required, name='dispatch')
class ServiceApplicationListView(ListView):
    model = ServiceApplication
    template_name = 'admin/service_application_list.html'
    context_object_name = 'service_applications'
    paginate_by = 10  # ✅ Enable pagination (10 per page)

    from datetime import datetime

    def get_queryset(self):
        qs = ServiceApplication.objects.prefetch_related('progress_logs', 'service', 'user').all()

        search_query = self.request.GET.get('search', '').strip()
        service_filter = self.request.GET.get('service', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        if search_query:
            qs = qs.filter(
                Q(user__phone_number__icontains=search_query) |
                Q(message__icontains=search_query) |
                Q(progress_logs__message__icontains=search_query) |
                Q(service__name__icontains=search_query) |
                Q(applied_at__icontains=search_query)
            ).distinct()

        if service_filter:
            qs = qs.filter(service__name__icontains=service_filter)

        if start_date:
            qs = qs.filter(applied_at__date__gte=start_date)

        if end_date:
            qs = qs.filter(applied_at__date__lte=end_date)

        return qs.order_by('-applied_at')


    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        applications = context['service_applications']

        progress_map = {}
        for app in applications:
            latest_progress = app.progress_logs.order_by('-updated_at').first()
            app.admin_status = latest_progress.get_status_display() if latest_progress else "N/A"
            app.admin_status_raw = latest_progress.status if latest_progress else ""
            app.admin_message = latest_progress.message if latest_progress else ""
            progress_map[app.id] = {log.status: log.message for log in app.progress_logs.all()}

        context['progress_status_choices'] = ServiceApplicationProgress.STATUS_CHOICES
        context['progress_json_map'] = json.dumps(progress_map)

        # Preserve search/filter values
        context['search_query'] = self.request.GET.get('search', '')
        context['service_filter'] = self.request.GET.get('service', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')

        # Optional: Provide service list for dropdown
        context['service_options'] = ServiceApplication.objects.values_list('service__name', flat=True).distinct()

        return context



# pdf
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.db.models import Q
from django.conf import settings
from .models import ServiceApplication
import os

@admin_role_required
def generate_service_application_pdf(request):
    # Register font
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'NotoSansBengali-Regular.ttf')
    pdfmetrics.registerFont(TTFont('Bangla', font_path))

    # Filters
    search_query = request.GET.get('search', '').strip()
    service_filter = request.GET.get('service', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    queryset = ServiceApplication.objects.select_related('service', 'user').prefetch_related('progress_logs')

    if search_query:
        queryset = queryset.filter(
            Q(user__phone_number__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(service__name__icontains=search_query)
        )
    if service_filter:
        queryset = queryset.filter(service__name__icontains=service_filter)
    if start_date:
        queryset = queryset.filter(applied_at__date__gte=start_date)
    if end_date:
        queryset = queryset.filter(applied_at__date__lte=end_date)

    # PDF setup
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="service_applications.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=30,
        bottomMargin=20
    )

    elements = []

    # Styles
    bangla_style = ParagraphStyle(
        name='Bangla',
        fontName='Bangla',
        fontSize=9,
        leading=12,
        alignment=0,
        wordWrap='CJK'
    )

    title_style = ParagraphStyle(
        name='Title',
        fontName='Bangla',
        fontSize=14,
        alignment=1,
        spaceAfter=16
    )

    elements.append(Paragraph("সার্ভিস অ্যাপ্লিকেশন রিপোর্ট", title_style))
    elements.append(Spacer(1, 12))

    # Table header
    data = [[
        Paragraph("ক্রম", bangla_style),
        Paragraph("ইউজার", bangla_style),
        Paragraph("সার্ভিস", bangla_style),
        Paragraph("মূল্য", bangla_style),
        Paragraph("ডিসকাউন্ট", bangla_style),
        Paragraph("পরিশোধ", bangla_style),
        Paragraph("বাকি", bangla_style),
        Paragraph("অবস্থা", bangla_style),
        Paragraph("মেসেজ", bangla_style),
        Paragraph("তারিখ", bangla_style),
    ]]

    for i, app in enumerate(queryset.order_by('-applied_at'), 1):
        latest_progress = app.progress_logs.order_by('-updated_at').first()
        status = latest_progress.get_status_display() if latest_progress else "N/A"
        message = latest_progress.message if latest_progress else "-"

        data.append([
            str(i),
            Paragraph(app.user.phone_number or "", bangla_style),
            Paragraph(app.service.name or "", bangla_style),
            f"{app.service.price:.2f}",
            f"{app.discount:.2f}",
            f"{app.amount_paid:.2f}",
            f"{app.balance:.2f}",
            Paragraph(status, bangla_style),
            Paragraph(message or "-", bangla_style),
            app.applied_at.strftime("%d-%b-%Y"),
        ])

    # Calculate column widths relative to available width
    total_width = doc.width
    col_widths = [
        total_width * 0.05,  # ক্রম
        total_width * 0.12,  # ইউজার
        total_width * 0.12,  # সার্ভিস
        total_width * 0.08,  # মূল্য
        total_width * 0.08,  # ডিসকাউন্ট
        total_width * 0.08,  # পরিশোধ
        total_width * 0.08,  # বাকি
        total_width * 0.12,  # অবস্থা
        total_width * 0.19,  # মেসেজ
        total_width * 0.08,  # তারিখ
    ]

    # Build table
    table = Table(data, repeatRows=1, colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0), (6,-1), 'CENTER'),
        ('ALIGN',(7,1), (8,-1), 'LEFT'),
        ('ALIGN',(9,1), (9,-1), 'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('FONTNAME', (0,0), (-1,-1), 'Bangla'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    return response






@method_decorator(admin_role_required, name='dispatch')
class EditLatestProgressView(View):
    def post(self, request, application_id):
        application = get_object_or_404(ServiceApplication, id=application_id)
        new_status = request.POST.get('status')
        new_message = request.POST.get('message', '').strip()

        if not new_status:
            messages.error(request, "স্ট্যাটাস ফিল্ডটি দেওয়া বাধ্যতামূলক।")
            return redirect('service_application_list')

        progress_qs = application.progress_logs.filter(status=new_status)
        if progress_qs.exists():
            progress = progress_qs.first()
            if new_message:
                progress.message = new_message
                progress.save()
        else:
            ServiceApplicationProgress.objects.create(
                application=application,
                status=new_status,
                message=new_message
            )

        messages.success(request, "স্ট্যাটাস এবং মেসেজ সফলভাবে আপডেট হয়েছে।")
        return redirect('service_application_list')


@method_decorator(admin_role_required, name='dispatch')
class EditDiscountView(View):
    def post(self, request, application_id):
        application = get_object_or_404(ServiceApplication, id=application_id)
        try:
            discount = int(request.POST.get('discount', 0))
            application.discount = discount
            application.save()
            messages.success(request, "ডিসকাউন্ট সফলভাবে আপডেট হয়েছে।")
        except ValueError:
            messages.error(request, "সঠিক ডিসকাউন্ট সংখ্যা দিন।")
        return redirect('service_application_list')




# from django.shortcuts import render
# from django.views.generic import ListView
# from django.core.paginator import Paginator
# from django.db.models import Q
# from .models import ServiceApplication
# from web_project import TemplateLayout, TemplateHelper  # Assuming you have these utilities

# from .models import ServiceApplication, ServiceApplicationProgress

# class ServiceApplicationListView(ListView):
#     model = ServiceApplication
#     template_name = 'admin/service_application_list.html'
#     context_object_name = 'service_applications'

#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         applications = ServiceApplication.objects.all().prefetch_related('progress_logs', 'service', 'user')
#         for app in applications:
#             latest_progress = app.progress_logs.order_by('-updated_at').first()
#             app.admin_status = latest_progress.get_status_display() if latest_progress else "N/A"
#             app.admin_status_raw = latest_progress.status if latest_progress else ""
#             app.admin_message = latest_progress.message if latest_progress else ""

#         context['service_applications'] = applications
#         context['progress_status_choices'] = ServiceApplicationProgress.STATUS_CHOICES  # ✅ Pass this
#         return context


# Timeline and admin message in service application table
# from django.views.generic.edit import UpdateView
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from .models import ServiceApplicationProgress, ServiceApplication
# from .forms import ServiceApplicationProgressForm

# class EditLatestProgressView(UpdateView):
#     model = ServiceApplicationProgress
#     form_class = ServiceApplicationProgressForm

#     def get_object(self, queryset=None):
#         application_id = self.kwargs.get('application_id')
#         application = get_object_or_404(ServiceApplication, id=application_id)
#         latest_progress = application.progress_logs.order_by('-updated_at').first()
#         return latest_progress

#     def form_valid(self, form):
#         messages.success(self.request, "অগ্রগতির তথ্য সফলভাবে আপডেট হয়েছে।")
#         return super().form_valid(form)

#     def get_success_url(self):
#         return redirect('service_application_list').url

# from django.views import View
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from .models import ServiceApplication, ServiceApplicationProgress

# class EditLatestProgressView(View):
#     def post(self, request, application_id):
#         application = get_object_or_404(ServiceApplication, id=application_id)
#         new_status = request.POST.get('status')
#         new_message = request.POST.get('message', '').strip()

#         if not new_status:
#             messages.error(request, "স্ট্যাটাস ফিল্ডটি দেওয়া বাধ্যতামূলক।")
#             return redirect('service_application_list')

#         # Progress log খোঁজো
#         progress_qs = application.progress_logs.filter(status=new_status)
#         if progress_qs.exists():
#             # আগের status, নতুন message দিলে সেটাই update হবে
#             progress = progress_qs.first()
#             if new_message:
#                 progress.message = new_message
#                 progress.save()
#         else:
#             # নতুন status দিলে নতুন log তৈরি হবে
#             ServiceApplicationProgress.objects.create(
#                 application=application,
#                 status=new_status,
#                 message=new_message
#             )

#         messages.success(request, "স্ট্যাটাস এবং মেসেজ সফলভাবে আপডেট হয়েছে।")
#         return redirect('service_application_list')






# Client payment from client site


# Service Pay Admin

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import ServiceApplication, ClientServices
from web_project import TemplateLayout, TemplateHelper  # Assuming you have these utilities

@method_decorator(admin_role_required, name='dispatch')
class ServicePayAdminListView(ListView):
    model = ServiceApplication
    template_name = 'service_pay/service_list_pay.html'  # New template name
    context_object_name = 'service_applications'

    def get_queryset(self):
        """
        Fetch ServiceApplications along with ClientServices, and filter if required.
        """
        return ServiceApplication.objects.select_related('service', 'user').all()

    def get_context_data(self, **kwargs):
        """
        Add custom context to the view, including layout and the filtered data.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Set the layout path if not already set in context
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context


# from django.shortcuts import render, get_object_or_404, redirect
# from django.views import View
# from django.contrib import messages
# from .forms import ServiceApplicationPaymentForm
# from .models import ServiceApplication

# class ServiceApplicationPaymentView(View):
#     def post(self, request, *args, **kwargs):
#         # Get the service application ID from the POST data
#         service_application_id = request.POST.get('service_application_id')
#         service_application = get_object_or_404(ServiceApplication, id=service_application_id)

#         # Process the payment form
#         form = ServiceApplicationPaymentForm(request.POST, instance=service_application)

#         if form.is_valid():
#             # Handle payment actions based on the form data (e.g., partial payment, full payment, etc.)
#             action_taken = form.cleaned_data['action_taken']
#             if action_taken == 'partial_payment':
#                 service_application.add_payment(
#                     form.cleaned_data['amount_paid'],
#                     form.cleaned_data['payment_message']
#                 )
#                 messages.success(request, "Partial payment applied successfully.")
#             elif action_taken == 'full_payment':
#                 service_application.mark_full_payment(
#                     form.cleaned_data['amount_paid'],
#                     form.cleaned_data['payment_message']
#                 )
#                 messages.success(request, "Full payment applied successfully.")
#             else:
#                 messages.error(request, "Invalid payment action.")

#             return redirect('service_pay_list')  # Redirect back to the service payment list

#         messages.error(request, "There was an error in your payment submission.")
#         return redirect('service_pay_list')  # Redirect to the same page if the form is invalid

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.views import View
# from .forms import ServiceApplicationPaymentForm
# from .models import ServiceApplication
# from web_project import TemplateLayout, TemplateHelper

# class ServiceApplicationPaymentView(View):
#     template_name = 'service_pay/service_application_payment.html'

#     def get(self, request, *args, **kwargs):
#         service_application_id = kwargs.get('service_application_id')

#         # Get the ServiceApplication object
#         service_application = get_object_or_404(ServiceApplication, id=service_application_id)

#         # Create the form with the current ServiceApplication data
#         form = ServiceApplicationPaymentForm(instance=service_application)

#         # Prepare the context data
#         context = TemplateLayout.init(self, {'form': form, 'service_application': service_application})

#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         service_application_id = kwargs.get('service_application_id')
#         service_application = get_object_or_404(ServiceApplication, id=service_application_id)

#         form = ServiceApplicationPaymentForm(request.POST, instance=service_application)
#         print(form.errors)
#         if form.is_valid():
#             action_taken = form.cleaned_data['action_taken']
#             amount_paid = form.cleaned_data['amount_paid']
#             payment_message = form.cleaned_data['payment_message']

#             # Only mark discount_used once
#             if not service_application.discount_used and form.cleaned_data['discount'] > 0:
#                 service_application.discount_used = True

#             # Process payment
#             if action_taken == 'partial_payment':
#                 service_application.add_payment(amount_paid, payment_message)
#                 messages.success(request, "Partial payment applied successfully.")
#             elif action_taken == 'full_payment':
#                 service_application.mark_full_payment(amount_paid, payment_message)
#                 messages.success(request, "Full payment applied successfully.")
#             else:
#                 # If no action, just save other fields
#                 form.save()

#             service_application.save()

#             return redirect('client-payment')

#         messages.error(request, "There was an error in your payment submission.")
#         return redirect('client-payment')








# from django.shortcuts import render
# from django.views.generic import ListView
# from django.core.paginator import Paginator
# from .models import ServiceApplication
# from django.db.models import Q
# from web_project import TemplateLayout, TemplateHelper  # Assuming these utilities exist in your project

# class ServiceApplicationAdminListView(ListView):
#     model = ServiceApplication
#     template_name = 'admin/service_application_admin_list.html'  # New template name
#     context_object_name = 'page_obj'

#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))

#         # Layout and template settings
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         # Pagination settings
#         per_page = 10  # Set how many entries per page
#         paginator = Paginator(self.get_queryset(), per_page)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['page_obj'] = page_obj

#         # Search query handling (optional)
#         search_query = self.request.GET.get('search', '')
#         context['search_query'] = search_query

#         return context

#     def get_queryset(self):
#         # Fetch all service applications
#         search_query = self.request.GET.get('search', '')
#         service_applications = ServiceApplication.objects.all()

#         if search_query:
#             service_applications = service_applications.filter(
#                 Q(service__name__icontains=search_query) |
#                 Q(user__phone_number__icontains=search_query)
#             )

#         return service_applications

from django.shortcuts import render
from django.views.generic import ListView
from .models import ServiceApplication
from web_project import TemplateLayout, TemplateHelper  # Assuming you have these utilities

@method_decorator(admin_role_required, name='dispatch')
class ServiceApplicationAdminListView(ListView):
    model = ServiceApplication
    template_name = 'admin/service_application_admin_list.html'  # New template name
    context_object_name = 'service_applications'

    def get_queryset(self):
        """
        Return all ServiceApplications without any filtering or pagination.
        Let the frontend handle pagination, search, and sorting.
        """
        return ServiceApplication.objects.all()

    def get_context_data(self, **kwargs):
        """
        Add custom context to the view, including layout and the filtered data.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Set the layout path if not already set in context
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context






# Client payment for their application to service

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import ServiceApplication
from .forms import ClientPaymentForm
from web_project import TemplateLayout, TemplateHelper


class ServiceApplicationPaymentView(TemplateView):
    template_name = 'client/service_application_payment.html'

    def get_context_data(self, **kwargs):
        """
        Add the necessary context to the template for rendering.
        This includes the service application data, the balance, and the form.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        service_application_id = kwargs.get('service_application_id')
        service_application = get_object_or_404(ServiceApplication, id=service_application_id, user=self.request.user)

        # Check if the service application exists and is associated with the user
        if not service_application:
            messages.error(self.request, "এই সেবা আবেদনটি পাওয়া যায়নি!")
            return redirect('applied_service_apply')

        # Initialize the payment form with the balance value as the initial amount
        form = ClientPaymentForm(initial={'amount': service_application.balance})

        # Set the context with the form and other data
        context['form'] = form
        context['service_application'] = service_application
        context['balance'] = service_application.balance  # Display the amount remaining to be paid

        # Add the layout context if needed
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context

    def post(self, request, *args, **kwargs):
        service_application_id = kwargs.get('service_application_id')
        service_application = get_object_or_404(ServiceApplication, id=service_application_id, user=request.user)

        # Check if the service application exists and is associated with the user
        if not service_application:
            messages.error(request, "এই সেবা আবেদনটি পাওয়া যায়নি!")
            return redirect('applied_service_apply')

        # Create a ClientPayment object and save it
        form = ClientPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the service for this payment
            payment = form.save(commit=False)
            payment.user = request.user
            payment.service = service_application  # Ensure the 'service' field is set
            payment.amount = form.cleaned_data['amount']  # Use the amount entered by the user

            # Save the payment
            payment.save()

            messages.success(request, "পেমেন্ট সফলভাবে সম্পন্ন হয়েছে, এডমিনের অনুমোদনের জন্য অপেক্ষা করুন।")
            # return redirect('client_payment_list')
            return redirect('payment_invoice', payment_id=payment.id)

        else:
            messages.error(request, "পেমেন্ট সাবমিট করার সময় একটি ত্রুটি ঘটেছে!")
            return render(request, self.template_name, {'form': form, 'service_application': service_application})




# Admin payment approval view

from django.views.generic import ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ClientPayment
from .forms import ClientPaymentAdminForm
from web_project import TemplateLayout, TemplateHelper
from datetime import datetime

@method_decorator(admin_role_required, name='dispatch')
class AdminClientPaymentListView(ListView):
    model = ClientPayment
    template_name = 'admin/client_payment_list.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_queryset(self):
        qs = ClientPayment.objects.select_related('user', 'service', 'service__service').order_by('-payment_date')

        user_query = self.request.GET.get('user', '')
        service_query = self.request.GET.get('service', '')
        search_query = self.request.GET.get('search', '')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if user_query:
            qs = qs.filter(user__phone_number__icontains=user_query)
        if service_query:
            qs = qs.filter(service__service__name__icontains=service_query)
        if search_query:
            qs = qs.filter(
                Q(transaction_id__icontains=search_query) |
                Q(message__icontains=search_query) |
                Q(admin_message__icontains=search_query)
            )
        if start_date:
            qs = qs.filter(payment_date__date__gte=start_date)
        if end_date:
            qs = qs.filter(payment_date__date__lte=end_date)

        return qs



    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = context.get('layout_path', 'layout_vertical.html')
        context['user_filter'] = self.request.GET.get('user', '')
        context['service_filter'] = self.request.GET.get('service', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['status_choices'] = ClientPayment.STATUS_CHOICES
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')


        # ✅ Add service list for filter dropdown
        context['service_options'] = ClientServices.objects.filter(status="active").order_by('name')

        return context

@method_decorator(admin_role_required, name='dispatch')
class EditClientPaymentView(UpdateView):
    model = ClientPayment
    form_class = ClientPaymentAdminForm
    template_name = 'admin/edit_client_payment.html'

    def form_valid(self, form):
        messages.success(self.request, "পেমেন্ট সফলভাবে আপডেট হয়েছে।")
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('admin_client_payment_list').url





from django.views.generic import TemplateView


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to tables/urls.py file for more pages.
"""


class TableView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context




# admin site notice make view

from .models import NoticePublic
from django.views.generic import ListView, CreateView
from .models import Notice, ClientServices
from .forms import NoticeForm, PublicNoticeForm  # Ensure this exists
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from web_project import TemplateLayout, TemplateHelper

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'client/notice_list.html'
    context_object_name = 'notices'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        context["notices"] = Notice.objects.select_related('service').order_by('-created_at')
        # queryset = Notice.objects.select_related('service').order_by('-created_at')
        # print("🟡 Notice Count:", queryset.count())  # 🔍 Check in console
        return context

@method_decorator(admin_role_required, name='dispatch')
class PublicNoticeListView(LoginRequiredMixin, ListView):
    model = NoticePublic
    template_name = 'client/notice_list_public.html'
    context_object_name = 'notices'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        context["notices"] = Notice.objects.select_related('service').order_by('-created_at')
        # queryset = Notice.objects.select_related('service').order_by('-created_at')
        # print("🟡 Notice Count:", queryset.count())  # 🔍 Check in console
        return context

# class NoticeListView(LoginRequiredMixin, ListView):
#     model = Notice
#     template_name = 'client/notice_list.html'
#     context_object_name = 'notices'

#     def get_queryset(self):
#         # Get service IDs applied by the current user
#         applied_service_ids = ServiceApplication.objects.filter(
#             user=self.request.user
#         ).values_list('service_id', flat=True)

#         # Return notices related to those services
#         return Notice.objects.filter(service__id__in=applied_service_ids).select_related('service').order_by('-created_at')

#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         # Pass filtered notices to template
#         context["notices"] = self.get_queryset()
#         return context


from django.http import HttpResponseForbidden

@method_decorator(admin_role_required, name='dispatch')
class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'admin/notice_create.html'
    success_url = reverse_lazy('notice_create')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Notice created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the notice.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["services"] = ClientServices.objects.all()
        context["notices"] = Notice.objects.select_related('service').order_by('-created_at')
        return context


from django.views.generic.edit import UpdateView

@method_decorator(admin_role_required, name='dispatch')
class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'admin/notice_create.html'
    success_url = reverse_lazy('notice_create')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Notice updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the notice.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["services"] = ClientServices.objects.all()
        context["notices"] = Notice.objects.select_related('service').order_by('-created_at')
        context["edit_mode"] = True
        return context



from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Notice, NoticePublic

@method_decorator(admin_role_required, name='dispatch')
class NoticeDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return HttpResponseForbidden("You do not have permission to delete this notice.")
        notice = get_object_or_404(Notice, pk=kwargs['pk'])
        notice.delete()
        messages.success(request, "নোটিশটি সফলভাবে মুছে ফেলা হয়েছে।")
        return HttpResponseRedirect(reverse('notice_create'))


# Public Notice
@method_decorator(admin_role_required, name='dispatch')
class PublicNoticeCreateView(LoginRequiredMixin, CreateView):
    model = NoticePublic
    form_class = PublicNoticeForm
    template_name = 'admin/public_notice_create.html'
    success_url = reverse_lazy('public_notice_create')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Public Notice created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the public notice.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["notices"] = NoticePublic.objects.order_by('-created_at')

        return context



@method_decorator(admin_role_required, name='dispatch')
class PublicNoticeUpdateView(LoginRequiredMixin, UpdateView):
    model = NoticePublic
    form_class = PublicNoticeForm
    template_name = 'admin/public_notice_create.html'
    success_url = reverse_lazy('public_notice_create')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "public Notice updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the public notice.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["notices"] = NoticePublic.objects.order_by('-created_at')
        context["edit_mode"] = True
        return context




@method_decorator(admin_role_required, name='dispatch')
class PublicNoticeDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.role != "admin":
            return HttpResponseForbidden("You do not have permission to delete this notice.")
        notice = get_object_or_404(NoticePublic, pk=kwargs['pk'])
        notice.delete()
        messages.success(request, "নোটিশটি সফলভাবে মুছে ফেলা হয়েছে।")
        return HttpResponseRedirect(reverse('public_notice_create'))
