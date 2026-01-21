from django.urls import path
from .views import FormWizardView, CVFormView, GuestCVView, GuestCVDetailView, PassportInfoCreateView, PassportInfoDetailView, GuestCVDetailView2
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path(
        "form/wizard_icons/",
        login_required(FormWizardView.as_view(template_name="form_wizard_icons.html")),
        name="form-wizard-icons",
    ),

    path('guest-cv/', login_required(GuestCVView.as_view()), name='cv-form-wizard'),
    path("my-cv/", login_required(GuestCVDetailView.as_view()), name="guest_cv_detail"),
    path("my-cv2/", login_required(GuestCVDetailView2.as_view()), name="guest_cv_detail2"),

    path('create-passport-info/', login_required(PassportInfoCreateView.as_view()), name='passport_info_create'),
    path('passport-info/details', login_required(PassportInfoDetailView.as_view()), name='passport_info_detail'),
    # path('passport-info/<int:pk>/', login_required(PassportInfoDetailView.as_view()), name='passport_info_detail'),

    # path("cv-wizard/", GuestCVWizard.as_view(FORMS), name="cv-form-wizard"),
]
