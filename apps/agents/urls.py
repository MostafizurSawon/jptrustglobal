from django.urls import path
from .views import ClientCvAgentCreateView

urlpatterns = [
    path('client-cv/create/', ClientCvAgentCreateView.as_view(), name='agent-cv-create'),
]
