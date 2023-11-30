from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import PrivacyPolicy, SiteSetting, ContactInfo, FooterCategoryTitle


# Favicon
def favicon_partial(request: HttpRequest):
    context = {
        'site_setting': SiteSetting.objects.first()
    }
    return render(request, 'core/favicon/fav.html', context)


# Header partial view
def header_site_component(request: HttpRequest):
    context = {
        'setting': SiteSetting.objects.first(),
    }

    return render(request, 'core/partials/header.html', context)


# Footer partial view
def footer_site_component(request: HttpRequest):
    context = {
        'setting': SiteSetting.objects.first(),
        'contact_info': ContactInfo.objects.first(),
        'footer_links': FooterCategoryTitle.objects.all()
    }
    return render(request, 'core/partials/footer.html', context)


# Site menu for mobile
def menu_component(request: HttpRequest):
    context = {
        'setting': SiteSetting.objects.first()
    }
    return render(request, 'core/partials/mobile_menu.html', context)


class PrivacyPolicyTemplateView(TemplateView):
    template_name = 'site/privacy-policy/PrivacyPolicyPage.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyTemplateView, self).get_context_data()
        context['privacy'] = PrivacyPolicy.objects.first()
        return context
