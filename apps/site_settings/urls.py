from django.urls import path
from .views import MiscPagesView, ContactView, ContactDataView, SiteSettingsUpdateView, SliderUpdateView, UpdateNoteView, ServiceDashboardView, DeleteServiceView, TrendingDashboardView, DeleteTrendingView, DeleteContactRowView, TestimonialCreateView, TestimonialUpdateView, DeleteTestimonialView, TeamCreateView, TeamUpdateView, DeleteTeamView
from django.contrib.auth.decorators import login_required
from .views import AppointmentDeleteView, AppointmentDashboardView, ChooseUpdateView, CvUpdateView, AppointmentNoticeUpdateView

urlpatterns = [
    path(
        "pages/misc/error/",
        MiscPagesView.as_view(template_name="pages_misc_error.html"),
        name="pages-misc-error",
    ),
    path(
        "pages/misc/under_maintenance/",
        MiscPagesView.as_view(template_name="pages_misc_under_maintenance.html"),
        name="pages-misc-under-maintenance",
    ),
    path(
        "pages/misc/comingsoon/",
        MiscPagesView.as_view(template_name="pages_misc_comingsoon.html"),
        name="pages-misc-comingsoon",
    ),
    path(
        "pages/misc/not_authorized/",
        MiscPagesView.as_view(template_name="pages_misc_not_authorized.html"),
        name="pages-misc-not-authorized",
    ),
    path('contact/', login_required(ContactView.as_view()), name='contact'),

    path('contact-dashboard/', login_required(ContactDataView.as_view()), name='contact_dashboard'),
    path('contact/update-note/', UpdateNoteView.as_view(), name='update_contact_note'),
    path('contact/delete-contact-row/', DeleteContactRowView.as_view(), name='delete_contact_row'),



    # path('contact/edit/<int:pk>/', views.contact_edit, name='contact_edit'),
    # path('contact/delete/<int:pk>/', views.contact_delete, name='contact_delete'),



    # Site settings
    path('site-settings/general', login_required(SiteSettingsUpdateView.as_view()), name='site_settings'),
    path('site-settings/sliders/', login_required(SliderUpdateView.as_view()), name='slider_update'),

    # Trending Video
    path('trending/', TrendingDashboardView.as_view(), name='trending_dashboard'),
    path('trending/delete/<int:pk>/', DeleteTrendingView.as_view(), name='trending_delete'),

    path('services/', ServiceDashboardView.as_view(), name='service_dashboard'),
    path('services/delete/<int:pk>/', DeleteServiceView.as_view(), name='service_delete'),

    # Our Team
    path('our-team/add', TeamCreateView.as_view(), name='our_team'),
    path('team/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_update'),
    path('team/<int:pk>/delete/', DeleteTeamView.as_view(), name='team_delete'),


    # cv frontend
    path('cv-section/', CvUpdateView.as_view(), name='cv_settings'),

    # Chose Us
    path('choose/', ChooseUpdateView.as_view(), name='choose_settings'),

    # Appointment URLs
    path('appointments/', AppointmentDashboardView.as_view(), name='appointment_dashboard'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),


     path('appointment-notice/', AppointmentNoticeUpdateView.as_view(), name='appointment_notice_settings'),

    # Testimonials
    path('testimonial/add/', TestimonialCreateView.as_view(), name='testimonial_create'),
    path('testimonial/<int:pk>/edit/', TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('testimonial/<int:pk>/delete/', DeleteTestimonialView.as_view(), name='testimonial_delete'),
]
