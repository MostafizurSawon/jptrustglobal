from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, AgentInfo
from .utils import generate_otp, generate_password, send_sms_jbd
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# from clients.models import PassportInfo, TravelAgencyCV

from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .forms import AgentInfoFormDashboard



import environ
env = environ.Env()
environ.Env.read_env()
# 9774 tjYD6Y77 31012011Sa

# BDBULKSMS_TOKEN = env("SMS_TOKEN")
TOKEN = env("JBD_SMS_TOKEN")

# import os
# TOKEN = os.getenv("JBDSMS_TOKEN")

# jbd sms
SENDER_ID = "8809617615010"  # customize sender id here, max 11 chars

OTP_VALIDITY_MINUTES = 5
OTP_RESEND_COOLDOWN_SECONDS = 60  # Cooldown between sending OTPs

def can_send_otp(user):
    # Check cooldown on last OTP sent
    if not user.otp_created_at:
        return True
    elapsed = (timezone.now() - user.otp_created_at).total_seconds()
    return elapsed > OTP_RESEND_COOLDOWN_SECONDS

def send_otp_sms(user, otp, password):
    message = f"আপনার ওটিপি: {otp}, লগইন ফোন নম্বর: {user.phone_number}, পাসওয়ার্ড: {password}"
    print("Sending otp...", TOKEN)
    return send_sms_jbd(user.phone_number, message, TOKEN, sender_id=SENDER_ID)




class GuestRegisterView(TemplateView):
    template_name = 'accounts/guest_register.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        return context

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone_number')

        if request.user.is_authenticated:
            return redirect('index')

        # 1. If active user exists
        if User.objects.filter(phone_number=phone, is_active=True).exists():
            messages.error(request, "A user with this phone number already exists.")
            return redirect('guest_register')

        # 2. If inactive user exists, resend OTP (with cooldown)
        user_qs = User.objects.filter(phone_number=phone, is_active=False)
        if user_qs.exists():
            user = user_qs.first()
            if not self.can_send_otp(user):
                messages.error(request, "Please wait before requesting another OTP.")
                return redirect('guest_register')

            otp = generate_otp()
            password = generate_password()
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.set_password(password)
            user.save(update_fields=['otp_code', 'otp_created_at', 'password'])

            status = send_otp_sms(user, otp, password)
            if status == "SENT":
                messages.success(request, "OTP resent successfully to your phone.")
                request.session['guest_phone'] = phone
                return redirect('guest_otp_verify')
            else:
                messages.error(request, "Failed to send OTP SMS. Please try again later.")
                return redirect('guest_register')

        # 3. Brand new user → send OTP first, then create user
        otp = generate_otp()
        password = generate_password()

        temp_user = User(
            phone_number=phone,
            role='guest',
            is_active=False,
            otp_code=otp,
            otp_created_at=timezone.now(),
        )
        temp_user.set_password(password)

        status = send_otp_sms(temp_user, otp, password)

        if status == "SENT":
            user = User.objects.create(
                phone_number=phone,
                role='guest',
                is_active=False,
                otp_code=otp,
                otp_created_at=timezone.now(),
            )
            user.set_password(password)
            user.save(update_fields=['password'])

            messages.success(request, "OTP sent successfully to your phone.")
            request.session['guest_phone'] = phone
            return redirect('guest_otp_verify')
        else:
            messages.error(request, "Failed to send OTP SMS. Please try again.")
            return redirect('guest_register')

    def can_send_otp(self, user):
        if not user.otp_created_at:
            return True
        elapsed = (timezone.now() - user.otp_created_at).total_seconds()
        return elapsed > 60  # OTP cooldown seconds




# agent register section (not admin)

class AgentRegisterView(TemplateView):
    template_name = 'accounts/guest_register.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        return context

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone_number')

        if request.user.is_authenticated:
            return redirect('index')

        # 1. If active user exists
        if User.objects.filter(phone_number=phone, is_active=True).exists():
            messages.error(request, "A user with this phone number already exists.")
            return redirect('guest_register')

        # 2. If inactive user exists, resend OTP (with cooldown)
        user_qs = User.objects.filter(phone_number=phone, is_active=False)
        if user_qs.exists():
            user = user_qs.first()
            if not self.can_send_otp(user):
                messages.error(request, "Please wait before requesting another OTP.")
                return redirect('guest_register')

            otp = generate_otp()
            password = generate_password()
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.set_password(password)
            user.save(update_fields=['otp_code', 'otp_created_at', 'password'])

            status = send_otp_sms(user, otp, password)
            if status == "SENT":
                messages.success(request, "OTP resent successfully to your phone.")
                request.session['guest_phone'] = phone
                return redirect('guest_otp_verify')
            else:
                messages.error(request, "Failed to send OTP SMS. Please try again later.")
                return redirect('guest_register')

        # 3. Brand new user → send OTP first, then create user
        otp = generate_otp()
        password = generate_password()

        temp_user = User(
            phone_number=phone,
            role='agent',
            is_active=False,
            otp_code=otp,
            otp_created_at=timezone.now(),
        )
        temp_user.set_password(password)

        status = send_otp_sms(temp_user, otp, password)

        if status == "SENT":
            user = User.objects.create(
                phone_number=phone,
                role='agent',
                is_active=False,
                otp_code=otp,
                otp_created_at=timezone.now(),
            )
            user.set_password(password)
            user.save(update_fields=['password'])

            messages.success(request, "OTP sent successfully to your phone.")
            request.session['guest_phone'] = phone
            return redirect('guest_otp_verify')
        else:
            messages.error(request, "Failed to send OTP SMS. Please try again.")
            return redirect('guest_register')

    def can_send_otp(self, user):
        if not user.otp_created_at:
            return True
        elapsed = (timezone.now() - user.otp_created_at).total_seconds()
        return elapsed > 60  # OTP cooldown seconds

# class AgentRegisterView(TemplateView):
#     template_name = 'agent/agent_register.html'

    # def get_context_data(self, **kwargs):
    #     # Initialize the context with TemplateLayout
    #     context = TemplateLayout.init(self, super().get_context_data(**kwargs))

    #     # Set the layout path if not already set in context
    #     context["layout_path"] = context.get("layout_path", "layout_vertical.html")

    #     return context

#     def post(self, request, *args, **kwargs):
#         phone = request.POST.get('phone_number')
#         print(f"Agent phone: {phone}")  # Debugging

#         # if request.user.role != 'admin':
#         #     messages.error(request, "You must be an admin to register agents.")
#         #     return redirect('home')

#         if User.objects.filter(phone_number=phone).exists():
#             messages.error(request, "An account with this phone number already exists.")
#             return redirect('agent_register')

#         # If inactive agent exists, resend OTP
#         user_qs = User.objects.filter(phone_number=phone, is_active=False, role='agent')
#         if user_qs.exists():
#             user = user_qs.first()
#             if not self.can_send_otp(user):
#                 messages.error(request, "Please wait before requesting another OTP.")
#                 return redirect('agent_register')

#             otp = generate_otp()
#             password = generate_password()
#             user.otp_code = otp
#             user.otp_created_at = timezone.now()
#             user.set_password(password)
#             user.save(update_fields=['otp_code', 'otp_created_at', 'password'])

#             # Resend OTP
#             status = send_otp_sms(user, otp, password)
#             if status == "SENT":
#                 messages.success(request, "OTP resent successfully to your phone.")
#                 request.session['agent_phone'] = phone
#                 return redirect('agent_otp_verify')
#             else:
#                 # Log the error response for debugging
#                 messages.error(request, f"Failed to send OTP SMS. Error: {status}")
#                 return redirect('agent_register')

#         # Brand new agent → send OTP first, then create user
#         otp = generate_otp()
#         password = generate_password()

#         temp_user = User(
#             phone_number=phone,
#             role='agent',
#             is_active=False,
#             otp_code=otp,
#             otp_created_at=timezone.now(),
#         )
#         temp_user.set_password(password)

#         print("t  ", temp_user)

#         # Attempt to send OTP SMS
#         status = send_otp_sms(temp_user, otp, password)
#         print("status ---->", status)
#         if status == "SENT":
#             user = User.objects.create(
#                 phone_number=phone,
#                 role='agent',
#                 is_active=False,
#                 otp_code=otp,
#                 otp_created_at=timezone.now(),
#             )
#             user.set_password(password)
#             user.save(update_fields=['password'])

#             messages.success(request, "OTP sent successfully to your phone.")
#             request.session['agent_phone'] = phone
#             return redirect('agent_otp_verify')
#         else:
#             # Log the error response for debugging
#             messages.error(request, f"Faileddd to send OTP SMS. Error: {status}")
#             return redirect('agent_register')

#     def can_send_otp(self, user):
#         if not user.otp_created_at:
#             return True
#         elapsed = (timezone.now() - user.otp_created_at).total_seconds()
#         return elapsed > 60  # OTP cooldown seconds



class AgentOtpVerifyView(TemplateView):
    template_name = 'agent/agent_otp_verify.html'

    def get_context_data(self, **kwargs):
        # Initialize the context with TemplateLayout
        context = TemplateLayout.init(self, {})

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        return context

    def post(self, request, *args, **kwargs):
        phone = request.session.get('agent_phone')

        if not phone:
            messages.error(request, "Session expired. Please start over.")
            return redirect('agent_register')

        otp = request.POST.get('otp')

        try:
            user = User.objects.get(phone_number=phone, role='agent')
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect('agent_register')

        if otp == user.otp_code:
            # OTP matches, activate the user
            if timezone.now() > user.otp_created_at + timedelta(minutes=5):
                messages.error(request, "OTP expired. Please request a new one.")
                return redirect('agent_register')

            user.is_active = True
            user.otp_code = None  # Clear OTP after successful verification
            user.otp_created_at = None
            user.save(update_fields=['is_active', 'otp_code', 'otp_created_at'])

            # Log the user in and redirect
            login(request, user)
            request.session.pop('agent_phone', None)
            messages.success(request, "Agent account activated. You can now log in.")
            return redirect('index')

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, self.template_name)


# Dashboard Agent Infos

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import AgentInfo
from .forms import AgentInfoFormDashboard, AgentInfoForm

class AgentInfoView(TemplateView):
    template_name = 'agent/agent_info_form.html'

    def get_context_data(self, **kwargs):
        # Initialize the context with TemplateLayout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # Check if the logged-in user already has existing agent info
        agent_info = AgentInfo.objects.filter(user=self.request.user).first()

        if agent_info:  # If agent info exists, pass it to the form for editing
            context['form'] = AgentInfoFormDashboard(instance=agent_info)
            context['is_edit'] = True  # This flag indicates that it's an edit operation
        else:  # If no agent info exists, pass a blank form for creating new agent info
            form = AgentInfoFormDashboard()
            form.instance.user = self.request.user  # Set the user field to the logged-in user
            form.instance.status = 'pending'  # Set the status to 'pending' by default
            context['form'] = form
            context['is_edit'] = False  # This flag indicates that it's a new submission

        return context

    def post(self, request, *args, **kwargs):
        # Handle form submission for creating or updating AgentInfo
        agent_info = AgentInfo.objects.filter(user=request.user).first()

        if agent_info:  # If agent info exists, update it
            form = AgentInfoFormDashboard(request.POST,request.FILES, instance=agent_info)
        else:  # If no agent info exists, create new
            form = AgentInfoFormDashboard(request.POST)

        # Automatically set the logged-in user for the 'user' field
        form.instance.user = request.user
        form.instance.status = 'pending'  # Set the status to "pending" by default

        if form.is_valid():
            form.save()
            messages.success(request, "Agent info saved successfully.")
            return redirect('agents_data')  # Redirect to the agent data page after saving
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(form=form))  # Re-render the form with errors


# from django.shortcuts import render
# from django.views.generic import ListView
# from apps.services.models import ServiceApplication
# from web_project import TemplateLayout, TemplateHelper  # Assuming you have these utilities

# class AgentsClient(ListView):
#     model = ServiceApplication
#     template_name = 'agent/agents_client_list.html'
#     context_object_name = 'service_applications'

#     def get_queryset(self):
#         """
#         Filter ServiceApplication instances by the logged-in user's PassportInfo.
#         """
#         # Get all service applications where passport_info is associated with the logged-in user
#         return ServiceApplication.objects.filter(passport_info__user=self.request.user)

#     def get_context_data(self, **kwargs):
#         """
#         Add custom context to the view, including layout and the filtered data.
#         """
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))

#         # Set the layout path if not already set in context
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

#         return context

from django.shortcuts import render
from django.views.generic import ListView
from apps.services.models import ServiceApplication
from web_project import TemplateLayout, TemplateHelper

class AgentsClient(ListView):
    model = ServiceApplication
    template_name = 'agent/agents_client_list.html'
    context_object_name = 'service_applications'

    def get_queryset(self):
        """
        Filter ServiceApplication instances by the logged-in user's PassportInfo.
        """
        # Get service applications where passport_info is associated with the logged-in user
        print('data --> ', self.request.user)
        return ServiceApplication.objects.filter(passport_info__agent__user=self.request.user)
        # return ServiceApplication.objects.filter(passport_info__user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add custom context to the view, including layout and the filtered data.
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Set the layout path if not already set in context
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        return context





# Agent sector for admin / hr_dashboard

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import AgentInfo, User
from .forms import AgentInfoEditForm

class AgentListView(ListView):
    model = AgentInfo
    template_name = 'admin/agent_list.html'
    context_object_name = 'page_obj'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # Check if the user is an admin or HR role
        if self.request.user.role not in ['admin', 'hr']:
            return HttpResponseForbidden("You do not have permission to access this page.")

        per_page = int(self.request.GET.get('per_page', 8))  # Default to 8 rows per page
        context['per_page'] = per_page

        paginator = Paginator(self.get_queryset(), per_page)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['search_query'] = self.request.GET.get('search', '')  # Keep the search query for the form

        return context

    def get_queryset(self):
        # Search functionality
        search_query = self.request.GET.get('search', '')
        agents = AgentInfo.objects.all()

        if search_query:
            agents = agents.filter(
                Q(user__phone_number__icontains=search_query) |
                Q(full_name__icontains=search_query)
            )
        return agents

    def post(self, request, *args, **kwargs):
        # Handle view, edit, delete requests
        if 'view' in request.POST:
            return self.view_agent(request)
        elif 'edit' in request.POST:
            return self.edit_agent(request)
        elif 'delete' in request.POST:
            return self.delete_agent(request)

    def view_agent(self, request):
        # Get the agent ID from the request
        agent_id = request.POST.get('agent_id')

        agent_info = get_object_or_404(AgentInfo, id=agent_id)

        # Initialize context with TemplateLayout
        context = TemplateLayout.init(self, {})

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # Pass the agent data to the view template
        context['agent_info'] = agent_info
        return render(request, 'admin/agent_view.html', context)

    def edit_agent(self, request):
        context = TemplateLayout.init(self, {})
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")
        agent_id = request.POST.get('agent_id')
        agent_info = get_object_or_404(AgentInfo, id=agent_id)

        print(agent_id, agent_info)

        # context['form'] = AgentInfoEditForm(request.POST or None, instance=agent_info)
        # context['is_edit'] = True

        form = AgentInfoEditForm(request.POST or None, instance=agent_info)
        context['form'] = AgentInfoEditForm(request.POST or None, instance=agent_info)
        context['is_edit'] = True

        print(form.errors)
        print(form.cleaned_data)

        if form.is_valid():
            form.save()
            messages.success(request, "Agent info updated successfully.")
            return redirect('agent_list')
        else:
            messages.error(request, "Please correct the errors below.")
            context['form'] = form
            context['agent_info'] = agent_info

            return render(request, 'admin/agent_info_form.html', context)

    def delete_agent(self, request):
        # Get the agent ID from the request
        agent_id = request.POST.get('agent_id')
        agent_info = get_object_or_404(AgentInfo, id=agent_id)

        # Initialize context with TemplateLayout for delete page
        context = TemplateLayout.init(self, {})
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # If the delete is confirmed, delete the agent info
        if request.POST.get('confirm_delete') == 'yes':
            agent_info.delete()
            messages.success(request, "Agent info deleted successfully.")
            return redirect('agent_list')  # Redirect to the agent list page after successful deletion
        else:
            # If not confirmed, display confirmation message
            context['agent_info'] = agent_info
            return render(request, 'admin/agent_list.html', {'page_obj': self.get_queryset(), 'confirm_delete': True})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import AgentInfo
from .forms import AgentInfoEditForm  # Assuming you have a form for editing agent info

class AgentInfoEditView(TemplateView):
    template_name = 'admin/agent_info_form.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # Check if the user is an admin or HR role
        if self.request.user.role not in ['admin', 'hr']:
            return HttpResponseForbidden("You do not have permission to access this page.")

        # Get the agent_id from the URL
        agent_id = kwargs.get('pk')  # Expecting the agent ID in the URL

        # Retrieve the agent's data
        agent_info = get_object_or_404(AgentInfo, id=agent_id)

        # Initialize the form with the existing agent data (for editing)
        form = AgentInfoEditForm(instance=agent_info)  # Pass the agent instance to pre-populate the form

        # Pass the agent info and the form to the context
        context['form'] = form
        context['is_edit'] = True  # This flag indicates that it's an edit operation
        context['agent_info'] = agent_info  # Pass the agent's data for display
        return context

    def post(self, request, *args, **kwargs):
        agent_id = kwargs.get('pk')
        agent_info = get_object_or_404(AgentInfo, id=agent_id)

        # Initialize the form with the POST data and agent instance
        form = AgentInfoEditForm(request.POST, request.FILES, instance=agent_info)  # Handling file uploads with request.FILES

        if form.is_valid():
            form.save()
            messages.success(request, "Agent info updated successfully.")
            return redirect('agent_list')  # Redirect to the agent list page after successful update
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'admin/agent_info_form.html', {'form': form, 'agent_info': agent_info})





from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from .models import AgentInfo, User
from .forms import AgentInfoForm

class AgentInfoAdminView(TemplateView):
    template_name = 'admin/agent_info_form.html'

    def get_context_data(self, **kwargs):
        # Initialize context with the base template
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Set the layout path if not already set in context
        context["layout_path"] = context.get("layout_path", "layout_vertical.html")

        # Check if the user is an admin or HR role
        if self.request.user.role not in ['admin', 'hr']:
            return redirect('guest_login')
            # return HttpResponseForbidden("You do not have permission to access this page.")

        # Get the list of users with the role 'agent'
        users = User.objects.filter(role='agent')
        context['users'] = users

        # Get the 'user' parameter from GET request to check if an agent is selected
        selected_user = self.request.GET.get('user_id', None)

        if selected_user:
            # If an agent is selected, populate the form with their data
            try:
                agent_info = AgentInfo.objects.get(user__id=selected_user)
                form = AgentInfoForm(instance=agent_info)  # Pre-populate the form with existing agent data
                context['is_edit'] = True  # This flag indicates that it's an edit operation
            except AgentInfo.DoesNotExist:
                # If the selected agent doesn't have AgentInfo, show a blank form
                form = AgentInfoForm(initial={'user': User.objects.get(id=selected_user)})
                context['is_edit'] = False  # This flag indicates that it's a new submission
        else:
            # If no agent is selected, show a blank form for creating new agent info
            form = AgentInfoForm()
            context['is_edit'] = False  # This flag indicates that it's for creating a new agent info

        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        # Check if the user is an admin or HR role
        if request.user.role not in ['admin', 'hr']:
            return HttpResponseForbidden("You do not have permission to access this page.")

        form = AgentInfoForm(request.POST)

        # Assign the user field based on the selected user
        selected_user = request.POST.get('user')
        if selected_user:
            form.instance.user = User.objects.get(id=selected_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Agent info created/updated successfully.")
            return redirect('agents_data')  # Redirect to the agent data page after successful creation or update
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(form=form))  # Re-render the form with errors




def normalize_phone_number(phone_number):
    # Strip spaces, hyphens, parentheses, or any other non-numeric characters
    phone_number = ''.join(c for c in phone_number if c.isdigit())

    # If phone number starts with 0, prepend the country code (880 for Bangladesh)
    if phone_number.startswith('0'):
        phone_number = '880' + phone_number[1:]  # Replace the leading 0 with country code

    # If the number already includes the country code, return it as it is
    elif not phone_number.startswith('880'):
        # If it's not starting with '880', we assume it's a wrong number or format.
        return None  # This handles invalid phone number formats

    return phone_number

# def guest_otp_verify(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         phone = request.session.get('guest_phone')

#         if not phone:
#             return redirect('guest_login')

#         try:
#             user = User.objects.get(phone_number=phone)
#         except User.DoesNotExist:
#             return render(request, 'accounts/guest_otp_verify.html', {'error': 'User not found. Please login again.'})

#         if user.is_active:
#             messages.info(request, "Your account is already activated. Please login.")
#             return redirect('guest_login')

#         # Check OTP expiry
#         if user.otp_created_at and timezone.now() > user.otp_created_at + timedelta(minutes=OTP_VALIDITY_MINUTES):
#             user.otp_code = None
#             user.otp_created_at = None
#             user.save(update_fields=['otp_code', 'otp_created_at'])
#             return render(request, 'accounts/guest_otp_verify.html', {'error': 'OTP expired. Please request again.'})

#         if entered_otp == user.otp_code:
#             user.is_active = True
#             user.otp_code = None
#             user.otp_created_at = None
#             user.save(update_fields=['is_active', 'otp_code', 'otp_created_at'])

#             # Create blank PassportInfo and CV if not exist
#             PassportInfo.objects.get_or_create(user=user)
#             TravelAgencyCV.objects.get_or_create(user=user)

#             messages.success(request, "Your account is activated. You can now login.")
#             request.session.pop('guest_phone', None)
#             return redirect('guest_login')
#         else:
#             return render(request, 'accounts/guest_otp_verify.html', {'error': 'Invalid OTP'})

#     return render(request, 'accounts/guest_otp_verify.html')

class GuestOtpVerifyView(TemplateView):
    template_name = 'accounts/guest_otp_verify.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        return context

    def post(self, request, *args, **kwargs):
        phone = request.session.get('guest_phone')

        if not phone:
            messages.error(request, "Session expired. Please start over.")
            return redirect('guest_login')

        otp = request.POST.get('otp')

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please login again.")
            return redirect('guest_login')

        if otp == user.otp_code:
            # OTP matches, activate the user
            if timezone.now() > user.otp_created_at + timedelta(minutes=5):
                messages.error(request, "OTP expired. Please request a new one.")
                return redirect('guest_register')

            user.is_active = True
            user.otp_code = None  # Clear OTP after successful verification
            user.otp_created_at = None
            user.save(update_fields=['is_active', 'otp_code', 'otp_created_at'])

            # Log the user in and redirect
            login(request, user)
            request.session.pop('guest_phone', None)
            messages.success(request, "Your account is activated. You can now log in.")
            return redirect('guest_login')

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'accounts/guest_otp_verify.html')


class LoginView(TemplateView):
    template_name = 'accounts/guest_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        return context

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')
        normalized_phone = normalize_phone_number(phone)

        user = authenticate(request, phone_number=normalized_phone, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "আপনার অ্যাকাউন্ট এখনো অ্যাক্টিভ নয়। অনুগ্রহ করে OTP যাচাই করুন।")
                return redirect('guest_otp_verify')

            login(request, user)
            messages.success(request, f"{user.phone_number} এর জন্য সফলভাবে লগইন হয়েছে।")
            return redirect('index')

        messages.error(request, "ফোন নম্বর বা পাসওয়ার্ড সঠিক নয়।")
        return self.render_to_response(self.get_context_data())

    # def redirect_by_role(self, user):
    #     role_redirect_map = {
    #         "admin": "admin:dashboard",
    #         "hr": "hr:dashboard",
    #         "agent": "agent:home",
    #         "guest": "clients:guest_cv_detail",
    #         "employee": "employee:home",
    #     }
    #     return redirect(role_redirect_map.get(user.role, "index"))

# def guest_login(request):
#     if request.user.is_authenticated:
#         return redirect('guest_dashboard')

#     if request.method == 'POST':
#         phone = request.POST.get('phone_number')
#         password = request.POST.get('password')

#         # Normalize the phone number
#         normalized_phone = normalize_phone_number(phone)

#         user = authenticate(request, phone_number=normalized_phone, password=password)

#         if user is not None and user.role == 'guest':
#             if not user.is_active:
#                 messages.error(request, "Your account is not activated yet. Please verify OTP.")
#                 return redirect('guest_otp_verify')
#             login(request, user)
#             return redirect('guest_dashboard')
#         else:
#             messages.error(request, "Invalid phone number or password.")

#     # return render(request, 'accounts/client_login.html')
#     return render(request, 'accounts/guest_login.html')

from django.views import View

class GuestForgotPasswordView(View):
    template_name = 'accounts/guest_forgot_password.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, kwargs)
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone_number')
        normalized_phone = normalize_phone_number(phone)

        if not normalized_phone:
            messages.error(request, "ফোন নম্বর সঠিক নয়। দয়া করে সঠিক নম্বর দিন (যেমন: 01XXXXXXXXX)।")
            return redirect('guest_forgot_password')

        try:
            user = User.objects.get(phone_number=normalized_phone, is_active=True, role='guest')
        except User.DoesNotExist:
            messages.error(request, "এই ফোন নম্বর দিয়ে কোন ব্যবহারকারী পাওয়া যায়নি।")
            return redirect('guest_forgot_password')

        if not can_send_otp(user):
            messages.error(request, "অনুগ্রহ করে কিছুক্ষণ অপেক্ষা করুন এবং পুনরায় চেষ্টা করুন।")
            return redirect('guest_forgot_password')

        otp = generate_otp()
        user.otp_code = otp
        user.otp_created_at = timezone.now()
        user.save(update_fields=['otp_code', 'otp_created_at'])

        message = f"আপনার পাসওয়ার্ড রিসেট OTP: {otp}"
        status = send_sms_jbd(user.phone_number, message, TOKEN, sender_id=SENDER_ID)

        print("==>", normalized_phone)  # ✅ now logs in correct format

        if status == "SENT":
            messages.success(request, "OTP সফলভাবে পাঠানো হয়েছে।")
            request.session['reset_phone'] = normalized_phone  # ✅ FIXED
            return redirect('guest_reset_password')
        else:
            messages.error(request, "OTP পাঠাতে ব্যর্থ হয়েছে। দয়া করে আবার চেষ্টা করুন।")
            return redirect('guest_forgot_password')




class GuestResetPasswordView(View):
    template_name = 'accounts/guest_reset_password.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, kwargs)
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        return context

    def get_user_from_session(self, request):
        phone = request.session.get('reset_phone')
        if not phone:
            return None
        try:
            return User.objects.get(phone_number=phone, is_active=True, role='guest')
        except User.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = self.get_user_from_session(request)
        if not user:
            messages.error(request, "Session expired. Please start password reset again.")
            return redirect('guest_forgot_password')
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        user = self.get_user_from_session(request)
        if not user:
            messages.error(request, "User not found. Please start over.")
            return redirect('guest_forgot_password')

        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not entered_otp or not new_password or not confirm_password:
            messages.error(request, "অনুগ্রহ করে সব ঘর পূরণ করুন।")
            return redirect('guest_reset_password')

        if new_password != confirm_password:
            messages.error(request, "পাসওয়ার্ড মিলছে না।")
            return redirect('guest_reset_password')

        if user.otp_code != entered_otp:
            messages.error(request, "ভুল OTP দেওয়া হয়েছে।")
            return redirect('guest_reset_password')

        if user.otp_created_at and timezone.now() > user.otp_created_at + timedelta(minutes=OTP_VALIDITY_MINUTES):
            messages.error(request, "OTP মেয়াদোত্তীর্ণ হয়েছে। পুনরায় অনুরোধ করুন।")
            return redirect('guest_forgot_password')

        # Reset password
        user.set_password(new_password)
        user.otp_code = None
        user.otp_created_at = None
        user.save(update_fields=['password', 'otp_code', 'otp_created_at'])

        messages.success(request, "পাসওয়ার্ড সফলভাবে রিসেট হয়েছে। এখন লগইন করুন।")
        request.session.pop('reset_phone', None)
        return redirect('guest_login')



# class LogoutGetAllowedView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         messages.success(request, "Logged Out Successfully.")
#         return self.post(request, *args, **kwargs)

# from django.contrib.auth.views import LogoutView
# from django.contrib import messages

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Logged out successfully.")
        return super().get(request, *args, **kwargs)




# def guest_otp_verify(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         phone = request.session.get('guest_phone')

#         if not phone:
#             return redirect('guest_login')

#         try:
#             user = User.objects.get(phone_number=phone)
#         except User.DoesNotExist:
#             context = {'error': 'User not found. Please login again.'}
#             return render(request, 'accounts/guest_otp_verify.html', context)

#         # Optional: Check if OTP expired (e.g., valid for 5 minutes)
#         if user.otp_created_at and timezone.now() > user.otp_created_at + timedelta(minutes=5):
#             user.otp_code = None
#             user.otp_created_at = None
#             user.save(update_fields=['otp_code', 'otp_created_at'])
#             context = {'error': 'OTP expired. Please request again.'}
#             return render(request, 'accounts/guest_otp_verify.html', context)

#         if entered_otp == user.otp_code:
#             # OTP matched: remove OTP fields
#             user.otp_code = None
#             user.otp_created_at = None
#             user.save(update_fields=['otp_code', 'otp_created_at'])

#             # Login user
#             login(request, user)
#             PassportInfo.objects.get_or_create(user=user)

#             # Clear phone from session
#             request.session.pop('guest_phone', None)

#             return redirect('guest_dashboard')
#         else:
#             context = {'error': 'Invalid OTP'}
#             return render(request, 'accounts/guest_otp_verify.html', context)



#     return render(request, 'accounts/guest_otp_verify.html')





# Guest change password from dashboard

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

class GuestChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/guest_change_password_dashboard.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context

    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')

        if not password1 or not password2:
            messages.error(request, "দয়া করে সব ঘর পূরণ করুন।")
            return self.render_to_response(self.get_context_data())

        if password1 != password2:
            messages.error(request, "পাসওয়ার্ডগুলো মিলছে না।")
            return self.render_to_response(self.get_context_data())

        user = request.user
        user.set_password(password1)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "পাসওয়ার্ড সফলভাবে পরিবর্তন হয়েছে।")
        return redirect('index')










@login_required
def guest_cv_list_panel(request):
    guest_cvs = TravelAgencyCV.objects.select_related('user').all()
    return render(request, 'dashboard/guest_cv_list_panel.html', {'guest_cvs': guest_cvs})

@login_required
def guest_cv_list(request):
    guest_cvs = TravelAgencyCV.objects.select_related('user').all()
    return render(request, 'dashboard/guest_cv_list.html', {'guest_cvs': guest_cvs})
    # return render(request, 'hr/hr_guest_cvs_list.html', {'guest_cvs': guest_cvs})

@login_required
def guest_cv_detail_by_pk(request, pk):
    cv = get_object_or_404(TravelAgencyCV, pk=pk)
    return render(request, 'dashboard/guest_cv.html', {'cv': cv})



# @login_required
# def hr_guest_cvs_list(request):
#     guest_cvs = TravelAgencyCV.objects.select_related('user').all()
#     return render(request, 'dashboard/hr_guest_cvs_list.html', {'guest_cvs': guest_cvs})
#     # return render(request, 'hr/hr_guest_cvs_list.html', {'guest_cvs': guest_cvs})



@login_required
def guest_dashboard(request):
    if request.user.role != 'guest':
        return redirect('home')

    # return render(request, 'accounts/guest_dashboard.html')
    return render(request, 'dashboard/guest_d.html')


@login_required
def guest_change_password(request):
    if request.user.role != 'guest':
        return redirect('home')

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password has been updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/guest_change_password.html', {'form': form})


@login_required
def view_guest_cv(request):

    return render(request, 'accounts/guest_cv.html')


@login_required
def view_guest_cv_by_pk(request, pk):
    cv = get_object_or_404(TravelAgencyCV, pk=pk)
    return render(request, 'dashboard/guest_cv.html', {'cv': cv})



# Role Based

def role_based_login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        if request.user.role == 'hr':
            return redirect('hr_dashboard')
        elif request.user.role == 'admin':
            # return redirect('admin_dashboard')
            return redirect('dashboard:admin_dashboard')
        else:
            return redirect('guest_dashboard')

    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone, password=password)

        # Allow all except guests here
        if user is not None and user.role != 'guest':
            login(request, user)
            print(user.role)
            if request.user.role == 'hr':
                return redirect('hr_dashboard')
            elif request.user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid phone number or password for this login.")

    return render(request, 'accounts/role_based_login.html')

@login_required
def admin_dashboard(request):
    if request.user.role == 'admin':
        # return render(request, 'accounts/admin_dashboard.html')
        return render(request, 'dashboard/admin_d.html')
    return redirect('home')

@login_required
def admin_index(request):
    if request.user.role != 'admin':
        return redirect('home')
    return render(request, 'dashboard/admin_index.html')




@login_required
def hr_dashboard(request):
    if request.user.role != 'hr':
        return redirect('home')


    # HR dashboard logic here
    return render(request, 'accounts/hr_dashboard.html')




@login_required
def hr_view_guests_passport(request):
    # Ensure only HR users can access
    if request.user.role != 'hr':
        return redirect('home')  # or permission denied page

    # Get all PassportInfo for users with role 'guest'
    guest_passports = PassportInfo.objects.filter(user__role='guest')

    context = {
        'guest_passports': guest_passports,
    }
    return render(request, 'hr/hr_guest_passports.html', context)


@login_required
def hr_guest_cvs_list(request):
    if request.user.role != 'hr':
        return redirect('home')  # or permission denied page
    guest_cvs = TravelAgencyCV.objects.select_related('user').all()
    return render(request, 'hr/hr_guest_cvs_list.html', {'guest_cvs': guest_cvs})




@login_required
def guest_cv_detail(request, pk):

    cv = TravelAgencyCV.objects.get(pk=pk)
    return render(request, 'hr/guest_cv_detail.html', {'cv': cv})



# from clients.forms import TravelAgencyCVForm

# @login_required
# def guest_cv_detail(request, pk):
#     if request.user.role != 'hr':
#         return redirect('home')

#     cv = get_object_or_404(TravelAgencyCV, pk=pk)

#     # Optional: confirm this cv belongs to a guest
#     if cv.user.role != 'guest':
#         return redirect('home')

#     if request.method == 'POST':
#         form = TravelAgencyCVForm(request.POST, request.FILES, instance=cv)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'CV updated successfully.')
#             return redirect('guest_cv_detail', pk=cv.pk)  # Or wherever you want to redirect
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = TravelAgencyCVForm(instance=cv)

#     return render(request, 'hr/guest_cv_edit.html', {'form': form, 'cv': cv})







# Template paid

# from django.views.generic import TemplateView
# from web_project import TemplateLayout


# # """
# # This file is a view controller for multiple pages as a module.
# # Here you can override the page view layout.
# # Refer to test/urls.py file for more pages.
# # """


# class accountsView(TemplateView):
#     # Predefined function
#     def get_context_data(self, **kwargs):
#         # A function to init the global layout. It is defined in web_project/__init__.py file
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))

#         return context


# from web_project import TemplateLayout
# from web_project.template_helpers.theme import TemplateHelper

# class accountsView(TemplateView):
#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         context.update({
#             "layout_path": TemplateHelper.set_layout("layout_blank.html", context),  # ✅ This line is MANDATORY
#         })
#         return context
