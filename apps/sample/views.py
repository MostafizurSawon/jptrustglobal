from django.views.generic import TemplateView
from web_project import TemplateLayout, TemplateHelper


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


class SampleView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


# Dashboard View for Service Application

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.views.generic import View
# from apps.form_wizard.models import PassportInfo
# from apps.services.models import ServiceApplication, ClientServices
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.contrib.auth.mixins import LoginRequiredMixin

# class ServiceApplyViewDashboard(View):
#     template_name = 'dashboard_crm.html'

#     def get(self, request, *args, **kwargs):
#         context = TemplateLayout.init(self, {})
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         print("--> ", request.user.role)
#         if request.user.role == 'guest':
#             print("User is a guest, redirecting to passport info creation.")
#         # Check if the user has a PassportInfo instance
#             if not hasattr(request.user, 'passport_info'):
#                 # If not, redirect to the create passport page
#                 return redirect('passport_info_create')  # Assuming 'passport_info_create' is the URL name for creating a passport

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
#         print("--> ", request.user.role)
#         if request.user.role == 'guest':
#             print("User is a guest, redirecting to passport info creationn.")
#             if not hasattr(request.user, 'passport_info'):
#                 # If not, redirect to create passport page
#                 messages.error(request, "You need to create your passport info first!")
#                 return redirect('passport_info_create')  # Redirect to the passport info creation page

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



from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from apps.services.models import ServiceApplication, ClientServices
from apps.form_wizard.models import PassportInfo
from django.core.paginator import Paginator
from django.db.models import Q

from apps.services.models import Notice  # Adjust path if Notice is elsewhere
from django.urls import reverse


class ServiceApplyViewDashboard(View):
    template_name = 'dashboard_crm.html'

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        # Get the latest active notice (if any)
        latest_notice = Notice.objects.filter(status='active').order_by('-created_at').first()
        context["latest_notice"] = latest_notice
        context["notice_create_url"] = reverse('notice')


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
                return redirect('service_apply')  # Redirect back to the service application page or success page
            except ClientServices.DoesNotExist:
                messages.error(request, "নির্বাচিত সেবা পাওয়া যায়নি।")
                return redirect('service_apply')

        messages.error(request, "ত্রুটি! অনুগ্রহ করে সেবা এবং বার্তা প্রদান করুন।")
        return redirect('service_apply')


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


from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated or getattr(user, 'role', None) not in allowed_roles:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator




# Expense

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import ExpenseCategory, Expense
from .forms import ExpenseCategoryForm, ExpenseForm
from web_project import TemplateLayout, TemplateHelper


# @method_decorator(admin_role_required, name='dispatch')
@method_decorator(role_required(['admin', 'hr']), name='dispatch')
class ExpenseDashboardView(View):
    template_name = 'expense/expense_dashboard.html'

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        context["category_form"] = ExpenseCategoryForm()
        context["expense_form"] = ExpenseForm()
        context["expense_categories"] = ExpenseCategory.objects.all()

        # Search & filter
        search_query = request.GET.get('search', '').strip()
        category_filter = request.GET.get('category', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        expenses = Expense.objects.select_related('category').order_by('-date')

        if search_query:
            expenses = expenses.filter(
                Q(ex_name__icontains=search_query) |
                Q(note__icontains=search_query) |
                Q(date__icontains=search_query)
            )

        if category_filter:
            expenses = expenses.filter(category_id=category_filter)

        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["expenses"] = page_obj
        context["search_query"] = search_query
        context["category_filter"] = category_filter
        context["start_date"] = start_date
        context["end_date"] = end_date
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        expense_id = kwargs.get("pk")  # Will be None for create

        if 'category_submit' in request.POST:
            form = ExpenseCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Expense category created successfully.")
            else:
                messages.error(request, "Failed to create expense category.")
            return redirect('create_expense')

        elif 'expense_submit' in request.POST:
            instance = None
            if expense_id:
                instance = Expense.objects.get(pk=expense_id)
            form = ExpenseForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                msg = "updated" if instance else "added"
                messages.success(request, f"Expense {msg} successfully.")
            else:
                messages.error(request, "Failed to submit expense form.")
            return redirect('create_expense')

        return self.get(request, *args, **kwargs)



from .models import ExpenseCategory
from .forms import ExpenseCategoryForm

from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q

# @method_decorator(admin_role_required, name='dispatch')
@method_decorator(role_required(['admin', 'hr']), name='dispatch')
class ExpenseCategoryView(View):
    template_name = "expense/expense_category_list.html"

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        search_query = request.GET.get('search', '').strip()
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        categories = ExpenseCategory.objects.all().order_by('-created_at')

        if search_query:
            categories = categories.filter(Q(name__icontains=search_query))

        if start_date:
            categories = categories.filter(created_at__date__gte=start_date)
        if end_date:
            categories = categories.filter(created_at__date__lte=end_date)

        paginator = Paginator(categories, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["categories"] = page_obj
        context["form"] = ExpenseCategoryForm()
        context["search_query"] = search_query
        context["start_date"] = start_date
        context["end_date"] = end_date
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")
        instance = ExpenseCategory.objects.get(pk=category_id) if category_id else None
        form = ExpenseCategoryForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            msg = "updated" if instance else "created"
            messages.success(request, f"Expense category {msg} successfully.")
        else:
            messages.error(request, "Failed to save category.")

        return redirect("expense_category_list")



from django.db.models import Sum


# @method_decorator(admin_role_required, name='dispatch')
# class ExpenseListView(View):
#     template_name = "expense/expense_list.html"

#     def get(self, request, *args, **kwargs):
#         context = TemplateLayout.init(self, {})
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
#         search_query = request.GET.get("q", "")
#         category_filter = request.GET.get("category")
#         start_date = request.GET.get("start_date")
#         end_date = request.GET.get("end_date")

#         # Base queryset
#         expenses_qs = Expense.objects.all().order_by("-date")

#         # Apply filters
#         if search_query:
#             expenses_qs = expenses_qs.filter(ex_name__icontains=search_query)

#         if category_filter:
#             expenses_qs = expenses_qs.filter(category_id=category_filter)

#         if start_date and end_date:
#             expenses_qs = expenses_qs.filter(date__range=[start_date, end_date])

#         # Total sum (for filtered queryset)
#         total_amount = expenses_qs.aggregate(total=Sum("amount"))["total"] or 0

#         # Pagination
#         paginator = Paginator(expenses_qs, 10)  # 10 per page
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)

#         context = {
#             "expenses": page_obj,
#             "expense_form": ExpenseForm(),
#             "categories": ExpenseCategory.objects.all(),
#             "search_query": search_query,
#             "category_filter": category_filter,
#             "start_date": start_date,
#             "end_date": end_date,
#             "total_expense": total_amount,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         expense_id = kwargs.get("pk")
#         instance = get_object_or_404(Expense, pk=expense_id) if expense_id else None

#         form = ExpenseForm(request.POST, instance=instance)

#         if form.is_valid():
#             form.save()
#             msg = "আপডেট সফল হয়েছে।" if instance else "নতুন ব্যয় যোগ করা হয়েছে।"
#             messages.success(request, msg)
#         else:
#             messages.error(request, "ডেটা সঠিক নয়, আবার চেষ্টা করুন।")

#         return redirect("expense_list")


# @method_decorator(admin_role_required, name='dispatch')
@method_decorator(role_required(['admin', 'hr']), name='dispatch')
class ExpenseListView(View):
    template_name = "expense/expense_list.html"

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        search_query = request.GET.get("search", "").strip()
        category_filter = request.GET.get("category", "")
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")

        expenses = Expense.objects.select_related("category").order_by("-date")

        if search_query:
            expenses = expenses.filter(
                Q(ex_name__icontains=search_query)
                | Q(note__icontains=search_query)
                | Q(date__icontains=search_query)
            )

        if category_filter:
            expenses = expenses.filter(category_id=category_filter)

        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        # 👇 Sum total of all filtered expenses
        total_amount = expenses.aggregate(total=Sum("amount"))["total"] or 0

        paginator = Paginator(expenses, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["expenses"] = page_obj
        context["expense_form"] = ExpenseForm()
        context["categories"] = ExpenseCategory.objects.all()
        context["search_query"] = search_query
        context["category_filter"] = category_filter
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["total_expense"] = total_amount  # 👈 Sum added to context
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        expense_id = request.POST.get("expense_id")
        expense_id = kwargs.get("pk")
        instance = get_object_or_404(Expense, pk=expense_id) if expense_id else None
        form = ExpenseForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
        else:
            messages.error(request, "Failed to update expense.")
        return redirect("expense_list")


# pdf

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from .models import Expense
from django.db.models import Q, Sum

@method_decorator(role_required(['admin', 'hr']), name='dispatch')
def generate_expense_pdf(request):
    search_query = request.GET.get("search", "").strip()
    category_filter = request.GET.get("category", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    expenses = Expense.objects.select_related("category").order_by("-date")
    if search_query:
        expenses = expenses.filter(
            Q(ex_name__icontains=search_query) |
            Q(note__icontains=search_query) |
            Q(date__icontains=search_query)
        )
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    total_amount = expenses.aggregate(total=Sum("amount"))["total"] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Expense Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # Table data with headers
    data = [["SL", "Name", "Category", "Amount (Taka)", "Date", "Note"]]
    for i, exp in enumerate(expenses, 1):
        data.append([
            str(i),
            exp.ex_name,
            exp.category.name,
            f"{exp.amount:.2f}",
            exp.date.strftime("%d-%b-%Y"),
            exp.note or "-"
        ])

    # Add total row
    data.append(["", "", "", f"Total: {total_amount:.2f} Taka", "", ""])

    # Create table and style
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))

    elements.append(table)
    doc.build(elements)

    return response


# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from django.db.models import Sum
# from .models import Expense, ExpenseCategory
# from django.utils.dateparse import parse_date

# def generate_expense_pdf(request):
#     search_query = request.GET.get("search", "").strip()
#     category_filter = request.GET.get("category", "")
#     start_date = request.GET.get("start_date", "")
#     end_date = request.GET.get("end_date", "")

#     expenses = Expense.objects.select_related("category").order_by("-date")

#     if search_query:
#         expenses = expenses.filter(
#             Q(ex_name__icontains=search_query)
#             | Q(note__icontains=search_query)
#             | Q(date__icontains=search_query)
#         )

#     if category_filter:
#         expenses = expenses.filter(category_id=category_filter)

#     if start_date:
#         expenses = expenses.filter(date__gte=start_date)

#     if end_date:
#         expenses = expenses.filter(date__lte=end_date)

#     total_amount = expenses.aggregate(total=Sum("amount"))["total"] or 0

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'

#     p = canvas.Canvas(response, pagesize=A4)
#     width, height = A4

#     y = height - 50
#     p.setFont("Helvetica-Bold", 14)
#     p.drawString(200, y, "Expense Report")

#     y -= 40
#     p.setFont("Helvetica", 10)
#     p.drawString(50, y, "SL")
#     p.drawString(80, y, "Name")
#     p.drawString(200, y, "Category")
#     p.drawString(300, y, "Amount")
#     p.drawString(370, y, "Date")
#     p.drawString(450, y, "Note")

#     y -= 20

#     for i, exp in enumerate(expenses, 1):
#         if y < 80:
#             p.showPage()
#             y = height - 50

#         p.drawString(50, y, str(i))
#         p.drawString(80, y, exp.ex_name[:20])
#         p.drawString(200, y, exp.category.name[:15])
#         p.drawString(300, y, f"{exp.amount} taka")
#         p.drawString(370, y, exp.date.strftime("%d-%b-%Y"))
#         p.drawString(450, y, exp.note[:20] if exp.note else "-")
#         y -= 18

#     y -= 30
#     p.setFont("Helvetica-Bold", 12)
#     p.drawString(50, y, f"Total Expenses: {total_amount} taka")

#     p.showPage()
#     p.save()

#     return response
