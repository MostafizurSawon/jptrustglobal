from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import CVForm
from .models import TravelAgencyCV
from web_project.template_helpers.theme import TemplateHelper
from web_project import TemplateLayout
from django.views.generic import TemplateView



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
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# class CVFormView(View):
#     def get_context_data(self, **kwargs):
#         # Manually create the context data for rendering
#         context = {}
#         return context

#     def get(self, request):
#         # Get or create the CV for the logged-in user
#         cv = getattr(request.user, 'cv', None)
#         if cv is None:
#             cv = TravelAgencyCV.objects.create(user=request.user)

#         # Initialize the form with the current user's data if it exists
#         form = CVForm(instance=cv)

#         # Get context data
#         context = self.get_context_data()

#         # Update context with the form
#         context.update({'form': form})

#         # Ensure TemplateLayout is called to set the layout path dynamically
#         context = TemplateLayout.init(self, context)

#         # Render the form wizard template with the provided context
#         return render(request, 'form_wizard_icons.html', context)

#     def post(self, request):
#         # Get or create the CV for the logged-in user
#         cv = getattr(request.user, 'cv', None)
#         if cv is None:
#             cv = TravelAgencyCV.objects.create(user=request.user)

#         # Instantiate the form with the POST data and current CV
#         form = CVForm(request.POST, instance=cv)

#         context = self.get_context_data()

#         # Update context with the form
#         context.update({'form': form})

#         # If the form is valid, save the CV (only at the last step)
#         if form.is_valid():
#             # Check if the form is on the last step
#             if 'submit' in request.POST:
#                 form.save()
#                 messages.success(request, "Your CV has been successfully saved.")
#                 return redirect('index')  # Redirect to the homepage after saving

#             # If it's not the final step, just proceed to the next step without saving
#             else:
#                 messages.info(request, "Step completed. Continue to the next step.")
#                 return render(request, 'form_wizard_icons.html', context)
#         else:
#             # If there are errors in the form, show them and allow the user to correct them
#             messages.error(request, "Please correct the errors below.")
#             return render(request, 'form_wizard_icons.html', context)

class CVFormView(View):
    def get_context_data(self, **kwargs):
        # Initialize context with layout_path
        context = TemplateLayout.init(self, {})
        return context

    def get(self, request):
        print("GET request received")
        # Get or create the CV for the logged-in user
        cv = getattr(request.user, 'cv', None)
        if cv is None:
            print("CV does not exist, creating new one")
            cv = TravelAgencyCV.objects.create(user=request.user)

        # Initialize the form with the current user's data if it exists
        form = CVForm(instance=cv)
        context = self.get_context_data()

        # Update context with the form
        context.update({'form': form})

        # Render the form wizard template with the provided context
        return render(request, 'form_wizard_icons.html', context)

    def post(self, request):
        print("POST request received")
        # Get or create the CV for the logged-in user
        cv = getattr(request.user, 'cv', None)
        if cv is None:
            print("CV does not exist, creating new one")
            cv = TravelAgencyCV.objects.create(user=request.user)

        # Initialize the form with POST data
        form = CVForm(request.POST, instance=cv)
        context = self.get_context_data()

        # Update context with the form
        context.update({'form': form})

        # Check if the form is valid
        if form.is_valid():
            print("Form is valid")
            # If the form is on the last step (when 'submit' is in POST)
            if 'submit' in request.POST:
                print("Submit button clicked, saving the form")
                form.save()  # Save the form to the database
                messages.success(request, "Your CV has been successfully saved.")
                return redirect('index')  # Redirect to the homepage after saving
            else:
                print("Not the final step, moving to the next step.")
                messages.info(request, "Step completed. Continue to the next step.")
                return render(request, 'form_wizard_icons.html', context)

        else:
            print("Form is not valid")
            # If there are errors, show them and allow the user to correct them
            messages.error(request, "Please correct the errors below.")
            return render(request, 'form_wizard_icons.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TravelAgencyCVForm
from .models import GuestCV
from web_project import TemplateLayout, TemplateHelper

class GuestCVView(LoginRequiredMixin, UpdateView):
    model = GuestCV
    form_class = TravelAgencyCVForm
    template_name = 'create_cv_guest.html'

    # Overriding dispatch method to check user role
    def dispatch(self, request, *args, **kwargs):
        print("Dispatch method called")
        # Check if the user is a guest
        if request.user.role != 'guest':
            messages.error(request, "You do not have permission to access this page.")
            print("User is not a guest, redirecting to index.")
            return redirect('index')  # Redirect to home or another page
        print("User is a guest, proceeding with dispatch.")
        # Continue with normal dispatch
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        print("get_object method called")
        # Check if the user has a GuestCV instance, otherwise create one
        obj, created = GuestCV.objects.get_or_create(user=self.request.user)
        print(f"get_object: GuestCV for user {self.request.user} exists or created: {created}")
        return obj

    def get_context_data(self, **kwargs):
        print("get_context_data method called")
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Ensure the layout is set explicitly
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        # Check if the user has data and pass it to the form instance
        try:
            guest_cv = GuestCV.objects.get(user=self.request.user)
            form = TravelAgencyCVForm(instance=guest_cv)  # Populate the form with existing data
            print("Existing GuestCV data found, form populated.")
        except GuestCV.DoesNotExist:
            form = TravelAgencyCVForm()  # If no data exists, show blank form
            print("No existing GuestCV data found, showing blank form.")

        context['form'] = form
        return context

    def form_valid(self, form):
        print("form_valid method called")
        # Save the form if valid
        form.instance.user = self.request.user
        form.save()

        messages.success(self.request, "Your CV has been saved successfully.")
        print("Form saved successfully, redirecting to cv-form-wizard.")
        return redirect('cv-form-wizard')  # Redirect after successful form submission

    def form_invalid(self, form):
        print("form_invalid method called")
        # Handle invalid form
        messages.error(self.request, "Please correct the errors below.")
        print("Form invalid, showing errors.")
        return self.render_to_response(self.get_context_data(form=form))




from django.views.generic.detail import DetailView

class GuestCVDetailView(LoginRequiredMixin, DetailView):
    model = GuestCV
    template_name = "guest_cv_detail.html"
    context_object_name = "cv"

    def get_object(self, queryset=None):
        return self.request.user.guest_cv  # assumes GuestCV is already created

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context

class GuestCVDetailView2(LoginRequiredMixin, DetailView):
    model = GuestCV
    template_name = "guest_cv_detail2.html"
    context_object_name = "cv"

    def get_object(self, queryset=None):
        return self.request.user.guest_cv  # assumes GuestCV is already created

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context








# from web_project import TemplateLayout
# from web_project.template_helpers.theme import TemplateHelper
# from formtools.wizard.views import SessionWizardView
# from django.shortcuts import redirect
# from .forms import PersonalInfoForm, FamilyJobInfoForm, SkillsFinalForm
# from .models import GuestCV

# FORMS = [
#     ("step1", PersonalInfoForm),
#     ("step2", FamilyJobInfoForm),
#     ("step3", SkillsFinalForm),
# ]

# TEMPLATES = {
#     "step1": "cv_wizard/step1_personal.html",
#     "step2": "cv_wizard/step2_family_job.html",
#     "step3": "cv_wizard/step3_skills_final.html",
# }

# class GuestCVWizard(SessionWizardView):
#     form_list = FORMS

#     def get_template_names(self):
#         return [TEMPLATES[self.steps.current]]

#     def get_context_data(self, form, **kwargs):
#         base_context = super().get_context_data(form=form, **kwargs)
#         context = TemplateLayout.init(self, base_context)
#         context["layout"] = "vertical"
#         context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
#         context["current_step"] = self.steps.current  # map to step1, step2, etc.
#         return context

#     def done(self, form_list, **kwargs):
#         data = {}
#         for form in form_list:
#             data.update(form.cleaned_data)

#         GuestCV.objects.update_or_create(
#             user=self.request.user,
#             defaults=data
#         )
#         return redirect("clients:guest_cv")



from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import PassportInfoForm
from web_project import TemplateLayout, TemplateHelper
from .models import PassportInfo

class PassportInfoCreateView(TemplateView):
    template_name = 'passport_info_form.html'

    def get_context_data(self, **kwargs):
        try:
            passport_info = PassportInfo.objects.get(user=self.request.user)
            form = PassportInfoForm(instance=passport_info, user=self.request.user)
        except PassportInfo.DoesNotExist:
            passport_info = None
            form = PassportInfoForm(user=self.request.user)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        context['form'] = form
        context['passport_info'] = passport_info
        return context

    def post(self, request, *args, **kwargs):
        try:
            passport_info = PassportInfo.objects.get(user=request.user)
            form = PassportInfoForm(request.POST, request.FILES, instance=passport_info, user=request.user)
        except PassportInfo.DoesNotExist:
            form = PassportInfoForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            # Explicitly set the user before saving
            passport_info = form.save(commit=False)
            passport_info.user = request.user
            passport_info.save()

            messages.success(request, "পাসপোর্ট তথ্য সফলভাবে সংরক্ষিত হয়েছে!")
            return redirect('passport_info_detail')
            # return redirect('passport_info_detail', pk=passport_info.pk)

        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)



from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import PassportInfo
from web_project import TemplateLayout, TemplateHelper  # Assuming you have these utilities

class PassportInfoDetailView(DetailView):
    model = PassportInfo
    template_name = 'passport_info_detail.html'
    context_object_name = 'passport_info'

    def get_object(self, queryset=None):
        """
        Override to return the PassportInfo object for the current logged-in user.
        """
        # Get the PassportInfo for the logged-in user
        return get_object_or_404(PassportInfo, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)

        # Pass additional context if necessary
        return context


# from django.shortcuts import render, get_object_or_404
# from django.views.generic import DetailView
# from apps.form_wizard.models import PassportInfo  # Import your PassportInfo model

# class PassportInfoDetailView(LoginRequiredMixin, DetailView):
#     model = PassportInfo
#     template_name = 'passport_info_detail.html'
#     context_object_name = 'passport_info'

#     def get_object(self, queryset=None):
#         # Retrieve PassportInfo for the logged-in user
#         passport_info = get_object_or_404(PassportInfo, user=self.request.user)
#         return passport_info

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Optional: Add additional context here if needed
#         return context






"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to form_wizard/urls.py file for more pages.
"""

# from web_project.template_helpers.theme import TemplateHelper
class FormWizardView(TemplateView):
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
