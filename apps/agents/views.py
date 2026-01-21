from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.agents.models import ClientCvAgent
from apps.agents.forms import ClientCvAgentForm
from web_project import TemplateLayout, TemplateHelper  # Adjust import if needed

class ClientCvAgentCreateView(LoginRequiredMixin, CreateView):
    model = ClientCvAgent
    form_class = ClientCvAgentForm
    template_name = 'cv/agent_cv_create.html'
    success_url = reverse_lazy('agent-cv-create')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "আপনার অ্যাকাউন্টে লগইন করুন")
            return redirect('guest_login')
        else:
            if request.user.role != 'agent':
                messages.error(request, "এই পৃষ্ঠাটি শুধুমাত্র এজেন্টদের জন্য অনুমোদিত।")
                return redirect('index')
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.agent = self.request.user.agent_info
        messages.success(self.request, "সিভি সফলভাবে সংরক্ষণ করা হয়েছে।")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        messages.error(self.request, "অনুগ্রহ করে সঠিকভাবে ফর্ম পূরণ করুন।")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["layout"] = "vertical"
        context["layout_path"] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context
