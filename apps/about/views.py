from django.views.generic.base import TemplateView

from .models import ReasonChoice, SpecializedField, CustomerComment


class AboutUsTemplateView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsTemplateView, self).get_context_data()
        context['reason_choices'] = ReasonChoice.objects.filter(is_active=True).all()
        context['specialized_fields'] = SpecializedField.objects.filter(is_active=True).all()
        context['customer_comments'] = CustomerComment.objects.filter(is_active=True).all()

        return context
