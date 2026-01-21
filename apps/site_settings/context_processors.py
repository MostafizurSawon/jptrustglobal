from .models import SiteSettings, Slider, Services, Trending, Testimonial, Team, Choose, Cv, AppointmentNotice
from apps.services.models import NoticePublic

def global_site_data(request):
    site_settings = SiteSettings.objects.first()
    slider = Slider.objects.first()
    services = Services.objects.all().order_by('id')
    trending_videos = Trending.objects.all().order_by('id')
    notices = NoticePublic.objects.filter(status='active').order_by('-created_at')
    testimonials = Testimonial.objects.all().order_by('-created_at')
    teams = Team.objects.all().order_by('-created_at')
    choose = Choose.objects.order_by('-created_at').first()
    cv = Cv.objects.first()
    note = AppointmentNotice.objects.first()


    return {
        'site_settings': site_settings or {},
        'slider_data': slider or {},
        'global_services': services,
        'global_trending': trending_videos,
        'public_notices': notices,
        'testimonials': testimonials,
        'teams': teams,
        'choose': choose,
        'cv': cv,
        'note': note,
    }
