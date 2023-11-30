from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import View

from .forms import ContactForm
from .models import Contact

from apps.site.models import ContactInfo


class ContactView(View):
    def get(self, request: HttpRequest):
        contact_form = ContactForm()
        context = {
            'contact_form': contact_form,
            'contact_info': ContactInfo.objects.filter(is_active=True).first()
        }
        return render(request, 'contact/contact.html', context)

    def post(self, request: HttpRequest):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            fullname = contact_form.cleaned_data.get('fullname')
            email = contact_form.cleaned_data.get('email')
            subject = contact_form.cleaned_data.get('subject')
            message = contact_form.cleaned_data.get('message')
            Contact.objects.create(fullname=fullname, email=email, subject=subject, message=message,
                                   is_read_by_admin=False)
            messages.success(request, 'پیام شما دریافت شد، با سپاس.')
            return redirect('contact')

        context = {'contact_form': contact_form}
        return render(request, 'contact/contact.html', context)
