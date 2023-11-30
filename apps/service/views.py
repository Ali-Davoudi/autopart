from django.views.generic.base import TemplateView

from .models import Service, ServiceDetail


class ServiceTemplateView(TemplateView):
    template_name = 'service/service.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceTemplateView, self).get_context_data()
        context['services'] = Service.objects.filter(is_active=True)
        context['service_detail'] = ServiceDetail.objects.filter(is_active=True).first()
        return context
