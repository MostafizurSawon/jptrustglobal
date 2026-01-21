from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.shortcuts import render, redirect, get_object_or_404

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class MiscPagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context


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




from django.shortcuts import render
from django.views import View
from .forms import ContactForm, ContactForm2
from django.contrib import messages
from web_project import TemplateLayout, TemplateHelper
@method_decorator(role_required(['admin', 'hr']), name='dispatch')
class ContactView(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = TemplateLayout.init(self, {'form': form})

        context["layout_path"] = context.get("layout_path", "layout_default.html")

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We've received your message and will get in touch shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Please enter a valid Bangladeshi mobile number (e.g., 01XXXXXXXXX)")
            context = TemplateLayout.init(self, {'form': form})
            context["layout_path"] = context.get("layout_path", "layout_default.html")
            return render(request, self.template_name, context)


# ফ্রন্টএন্ড থেকে যোগাযোগ ফর্ম
class ContactViewFront(View):
    template_name = 'contact-us.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = TemplateLayout.init(self, {'form': form})
        context["layout_path"] = context.get("layout_path", "layout_default.html")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("ContactViewFront থেকে POST অনুরোধ এসেছে")
        form = ContactForm(request.POST)
        print(form.errors)  # ফর্ম ত্রুটি ডিবাগিংয়ের জন্য
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We've received your message and will get in touch shortly.")
            return redirect('contact-home')  # সফলতার পর কন্টাক্ট হোমে রিডাইরেক্ট
        else:
            messages.error(request, "Please correct the error.")
            context = TemplateLayout.init(self, {'form': form})
            context["layout_path"] = context.get("layout_path", "layout_default.html")
            return render(request, self.template_name, context)


# ফ্রন্টএন্ড থেকে সাধারণ প্রশ্ন/জিজ্ঞাসা
class QueryViewFront(View):
    template_name = 'query_form.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm2()
        context = TemplateLayout.init(self, {'form': form})
        context["layout_path"] = context.get("layout_path", "layout_default.html")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # print("QueryViewFront theke req eseche")
        form = ContactForm2(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! We've received your message and will get in touch shortly.")
            return redirect('query_form')
        else:
            messages.error(request, "Please correct the error.")
            context = TemplateLayout.init(self, {'form': form})
            context["layout_path"] = context.get("layout_path", "layout_default.html")
            return render(request, self.template_name, context)




from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Contact
from web_project import TemplateLayout, TemplateHelper
from django.http import HttpResponseForbidden

@method_decorator(role_required(['admin', 'hr']), name='dispatch')
class ContactDataView(View):
    template_name = 'contact_data.html'

    def get(self, request, *args, **kwargs):
        contacts = Contact.objects.all().order_by('-created_at')

        # Filters
        purpose_filter = request.GET.get('purpose')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        search_query = request.GET.get('search')

        if purpose_filter and purpose_filter != 'all':
            contacts = contacts.filter(purpose=purpose_filter)

        if start_date:
            contacts = contacts.filter(created_at__date__gte=start_date)

        if end_date:
            contacts = contacts.filter(created_at__date__lte=end_date)

        if search_query:
            contacts = contacts.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(message__icontains=search_query)
            )

        paginator = Paginator(contacts, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'contacts': page_obj,
            'purpose_filter': purpose_filter or 'all',
            'start_date': start_date or '',
            'end_date': end_date or '',
            'search_query': search_query or '',
        }

        context = TemplateLayout.init(self, context)
        context["layout_path"] = context.get("layout_path", "layout_default.html")

        return render(request, self.template_name, context)



#  Add note

from django.http import JsonResponse
from django.views import View
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from .models import Contact
from .forms import ContactNoteForm

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(role_required(['admin', 'hr']), name='dispatch')
class UpdateNoteView(View):
    def post(self, request, *args, **kwargs):

        contact_id = request.POST.get('id')
        contact = Contact.objects.filter(id=contact_id).first()

        if not contact:
            return JsonResponse({'success': False, 'error': 'Contact information not found!'}, status=404)

        form = ContactNoteForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return JsonResponse({'success': True, 'note': contact.note})
        else:
            messages.error(request, "Note update failed!")
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)



#  Delete row of contact data
@method_decorator(csrf_exempt, name='dispatch')
class DeleteContactRowView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return JsonResponse({'success': False, 'error': 'No Permission'}, status=403)

        contact_id = request.POST.get('id')
        contact = Contact.objects.filter(id=contact_id).first()

        if not contact:
            return JsonResponse({'success': False, 'error': 'Contact information not found!'}, status=404)

        contact.delete()  # 🔥 delete the entire row
        messages.success(request, "Successfully deleted!")
        return JsonResponse({'success': True})





# Site settings



from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import SiteSettings
from .forms import SiteSettingsForm
from web_project import TemplateLayout, TemplateHelper


@method_decorator(admin_role_required, name='dispatch')
class SiteSettingsUpdateView(UpdateView):
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = 'admin/site_settings.html'
    success_url = reverse_lazy('site_settings')

    def get_object(self):
        return SiteSettings.objects.first()  # Assumes a single settings instance

    def form_valid(self, form):
        messages.success(self.request, "Site settings updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Site Settings"
        return context



from .models import Slider
from .forms import SliderForm

@method_decorator(admin_role_required, name='dispatch')
class SliderUpdateView(UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'admin/slider_update.html'
    success_url = reverse_lazy('slider_update')

    def get_object(self):
        return Slider.objects.first()

    def form_valid(self, form):
        messages.success(self.request, "Sliders updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Slider update"
        return context





from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Services
from .forms import ServicesForm
from web_project import TemplateLayout, TemplateHelper






@method_decorator(admin_role_required, name='dispatch')
class ServiceDashboardView(View):
    template_name = 'admin/service_dashboard.html'

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        # Search/filter
        search_query = request.GET.get('search', '').strip()
        services = Services.objects.all().order_by('-id')

        if search_query:
            services = services.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Pagination
        paginator = Paginator(services, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["services"] = page_obj
        context["search_query"] = search_query
        context["form"] = ServicesForm()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        service_id = request.POST.get("service_id")
        instance = get_object_or_404(Services, pk=service_id) if service_id else None

        form = ServicesForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            msg = "updated" if instance else "created"
            messages.success(request, f"Service {msg} successfully.")
        else:
            messages.error(request, "Failed to save service.")
        return redirect("service_dashboard")


@method_decorator(admin_role_required, name='dispatch')
class DeleteServiceView(View):
    def post(self, request, pk, *args, **kwargs):
        service = get_object_or_404(Services, pk=pk)
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect("service_dashboard")



#  Tredning Video

from .models import Trending
from .forms import TrendingForm

@method_decorator(admin_role_required, name='dispatch')
class TrendingDashboardView(View):
    template_name = 'admin/trending_dashboard.html'

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, {})
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        search_query = request.GET.get('search', '').strip()
        trendings = Trending.objects.all().order_by('-id')

        if search_query:
            trendings = trendings.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(link__icontains=search_query)
            )

        paginator = Paginator(trendings, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["trendings"] = page_obj
        context["search_query"] = search_query
        context["form"] = TrendingForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        trending_id = request.POST.get("trending_id")
        instance = get_object_or_404(Trending, pk=trending_id) if trending_id else None

        form = TrendingForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            msg = "updated" if instance else "created"
            messages.success(request, f"Trending item {msg} successfully.")
        else:
            messages.error(request, "Failed to save trending item.")
        return redirect("trending_dashboard")

@method_decorator(admin_role_required, name='dispatch')
class DeleteTrendingView(View):
    def post(self, request, pk, *args, **kwargs):
        trending = get_object_or_404(Trending, pk=pk)
        trending.delete()
        messages.success(request, "Trending item deleted successfully.")
        return redirect("trending_dashboard")



from .models import Team
from .forms import TeamForm

@method_decorator(admin_role_required, name='dispatch')
class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'admin/team_list.html'
    success_url = reverse_lazy('our_team')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Team Members"
        context["teams"] = Team.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Team member added successfully.")
        return super().form_valid(form)

@method_decorator(admin_role_required, name='dispatch')
class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'admin/team_list.html'
    success_url = reverse_lazy('our_team')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Edit Team Member"
        context["teams"] = Team.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Team member updated successfully.")
        return super().form_valid(form)

@method_decorator(admin_role_required, name='dispatch')
class DeleteTeamView(View):
    def post(self, request, pk, *args, **kwargs):
        team = get_object_or_404(Team, pk=pk)
        team.delete()
        messages.success(request, "Team member deleted successfully.")
        return redirect('our_team')



from .forms import TestimonialForm
from .models import Testimonial
from django.views.generic.edit import CreateView

@method_decorator(admin_role_required, name='dispatch')
class TestimonialCreateView(CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'admin/testimonial_list.html'
    success_url = reverse_lazy('testimonial_create')

    def form_valid(self, form):
        messages.success(self.request, "New testimonial added!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "New Testimonial Add"
        context["testimonials"] = Testimonial.objects.all().order_by('-id')
        return context


@method_decorator(admin_role_required, name='dispatch')
class TestimonialUpdateView(UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'admin/testimonial_list.html'
    success_url = reverse_lazy('testimonial_create')

    def form_valid(self, form):
        messages.success(self.request, "Testimonial updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Update Testimonial"
        context["testimonials"] = Testimonial.objects.all().order_by('-id')
        return context



@method_decorator(admin_role_required, name='dispatch')
class DeleteTestimonialView(View):
    def post(self, request, pk, *args, **kwargs):
        testimonial = get_object_or_404(Testimonial, pk=pk)
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully.")
        return redirect('testimonial_create')




# Appointment View
from django.views.generic import CreateView, ListView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from .models import Appointment
from .forms import AppointmentForm

@method_decorator(admin_role_required, name='dispatch')
class AppointmentDashboardView(View):
    template_name = 'admin/appointment_dashboard.html'

    def get(self, request, *args, **kwargs):
        edit_id = request.GET.get("edit")
        instance = get_object_or_404(Appointment, pk=edit_id) if edit_id else None
        form = AppointmentForm(instance=instance)

        context = self._build_context(request)
        context["form"] = form
        context["edit_id"] = edit_id
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get("appointment_id")
        instance = get_object_or_404(Appointment, pk=instance_id) if instance_id else None

        form = AppointmentForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, "Appointment saved successfully.")
            return redirect("appointment_dashboard")
        else:
            context = self._build_context(request)
            context["form"] = form  # Invalid form with errors
            return render(request, self.template_name, context)

    def _build_context(self, request):
        search = request.GET.get('search', '').strip()
        status = request.GET.get('status', '')

        queryset = Appointment.objects.all().order_by('-created_at')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(mobile_number__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)

        paginator = Paginator(queryset, 10)
        page = request.GET.get('page')
        appointments = paginator.get_page(page)

        context = {
            "appointments": appointments,
            "form": AppointmentForm(),
            "search_query": search,
            "selected_status": status,
        }

        context = TemplateLayout.init(self, context)
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Appointments"
        return context

@method_decorator(admin_role_required, name='dispatch')
class AppointmentDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        return redirect('appointment_dashboard')



# cv frontend
from .models import Cv
from .forms import CvForm

@method_decorator(admin_role_required, name='dispatch')
class CvUpdateView(UpdateView):
    model = Cv
    form_class = CvForm
    template_name = 'admin/cv_form.html'
    success_url = reverse_lazy('cv_settings')

    def get_object(self):
        return Cv.objects.first() or Cv.objects.create()

    def form_valid(self, form):
        messages.success(self.request, "CV section updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Form submission failed. Please fix the errors.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "CV Section"
        return context


# Chose us

from .models import Choose
from .forms import ChooseForm

@method_decorator(admin_role_required, name='dispatch')
class ChooseUpdateView(UpdateView):
    model = Choose
    form_class = ChooseForm
    template_name = 'admin/choose_form.html'
    success_url = reverse_lazy('choose_settings')

    def get_object(self):
        return Choose.objects.first() or Choose.objects.create()

    def form_valid(self, form):
        messages.success(self.request, "Choose section updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error. Please check the form.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Why Choose Us"
        return context



# Public Appointment
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentFormPublic
from web_project import TemplateLayout, TemplateHelper

class AppointmentPublicCreateView(View):
    template_name = "office_appointment.html"

    def get(self, request, *args, **kwargs):
        form = AppointmentFormPublic()
        context = TemplateLayout.init(self, {'form': form})
        context["layout_path"] = context.get("layout_path", "layout_default.html")
        context["page_title"] = "Appointment Form"
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AppointmentFormPublic(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointments submitted successfully.")
            return redirect("appointment_public")
        else:
            messages.error(request, "Please correct the errors.")
            context = TemplateLayout.init(self, {'form': form})
            context["layout_path"] = context.get("layout_path", "layout_default.html")
            return render(request, self.template_name, context)


# Appointment er dane 3 ta notice
from .models import AppointmentNotice
from .forms import AppointmentNoticeForm

@method_decorator(admin_role_required, name='dispatch')
class AppointmentNoticeUpdateView(UpdateView):
    model = AppointmentNotice
    form_class = AppointmentNoticeForm
    template_name = 'admin/appointment_notice_form.html'
    success_url = reverse_lazy('appointment_notice_settings')

    def get_object(self):
        return AppointmentNotice.objects.first() or AppointmentNotice.objects.create()

    def form_valid(self, form):
        messages.success(self.request, "Appointment notice saved successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context["page_title"] = "Appointment notice settings"
        return context
