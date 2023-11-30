from django import forms
from django.core import validators

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from ckeditor.widgets import CKEditorWidget

from utils.validators import validate_email, validate_rich_text


class ContactForm(forms.Form):
    fullname = forms.CharField(
        label='نام و نام خانوادگی * ',
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی', 'name': 'name'}),
        error_messages={'required': 'لطفا قسمت نام و نام خانوادگی را خالی نگذارید!'},
        validators=[
            validators.MaxLengthValidator(40, 'نام و نام خانوادگی نمی تواند بیشتر از 40 کاراکتر باشد.')
        ]
    )
    email = forms.EmailField(
        label='آدرس ایمیل * ',
        widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی', 'name': 'email'}),
        error_messages={'required': 'لطفا قسمت ایمیل را خالی نگذارید!'},
        validators=[validate_email]
    )
    subject = forms.CharField(
        label='موضوع پیام (اختیاری) ',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'موضوع پیام', 'name': 'subject'}),
    )
    message = forms.CharField(
        label='پیام *',
        widget=CKEditorWidget(config_name='contact'),
        required=True,
        validators=[validate_rich_text],
        error_messages={'required': 'لطفا پیام خود را وارد کنید.'},
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
