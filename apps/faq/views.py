from django.views.generic.base import TemplateView

from .models import Faq


class FaqTemplateView(TemplateView):
    template_name = 'faq/faq.html'

    def get_context_data(self, **kwargs):
        context = super(FaqTemplateView, self).get_context_data()
        context['faqs'] = Faq.objects.filter(is_active=True)
        return context
