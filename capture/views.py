from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from . import forms


class LeadDetailView(CreateView):
    """Capture lead details."""
    template_name = 'capture/lead_detail.html'
    form_class = forms.LeadDetailForm
    success_url = reverse_lazy('thanks')


class Thanks(TemplateView):
    template_name = 'capture/thanks.html'
