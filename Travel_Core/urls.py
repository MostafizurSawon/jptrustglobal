"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views
from apps.site_settings.views import ContactViewFront, QueryViewFront

from django.contrib.auth.decorators import login_required
from apps.site_settings.views import AppointmentPublicCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('blogs/', views.blogs, name='blogs'),
    # path('contact-us/', views.contact, name='contact-home'),
    path('contact-us/', ContactViewFront.as_view(), name='contact-home'),
    # path('contact-us/', views.contact, name='contact-home'),
    path('about/', views.about, name='about'),
    path('video_details/', views.video, name='video_home'),
    path('all-notices/', views.public_notices, name='public_notices'),


    # path('appointment/', views.appointment, name='appointment'),
    path('appointment/', AppointmentPublicCreateView.as_view(), name='appointment_public'),


    # General query all
    path('general-query/', QueryViewFront.as_view(), name='query_form'),



    path("admin/", admin.site.urls),
    # starter urls
    path("dashboard/", include("apps.sample.urls")),
    # pages urls
    path("dashboard/", include("apps.site_settings.urls")),
    # FormWizard urls
    path("dashboard/", include("apps.form_wizard.urls")),
    path("dashboard/", include("apps.services.urls")),
    path("dashboard/", include("apps.clients.urls")),

    path("", include("apps.accounts.urls")),
    path("", include("apps.guest_docs.urls")),
    path("agent-dashboard/", include("apps.agents.urls")),
    # auth urls
    # path("", include("auth.urls")),
]
if settings.DEBUG or True:  # ⚠️ True দিলেই সবসময় serve করবে
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
