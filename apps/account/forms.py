from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from utils.validators import validate_email, validate_password_strenght


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='پست الکترونیکی * ',
        widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}),
        error_messages={'required': 'لطفا پست الکترونیکی خود را وارد نمایید.'},
        validators=[validators.MinLengthValidator(10, 'ایمیل وارد شده نباید کمتر از 10 کاراکتر باشد.'),
                    validators.MaxLengthValidator(80, 'ایمیل وارد شده نمی تواند بیشتر از 80 کاراکتر باشد.'),
                    validate_email
                    ]
    )
    password = forms.CharField(
        label='کلمه عبور * ',
        widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور'}),
        error_messages={'required': 'لطفا کلمه عبور را وارد نمایید.'},
        validators=[validators.MinLengthValidator(5, 'کلمه عبور باید بیشتر از 5 کاراکتر باشد.'),
                    validate_password_strenght]
    )
    confrim_password = forms.CharField(
        label='تکرار کلمه عبور * ',
        widget=forms.PasswordInput(attrs={'placeholder': 'تکرار کلمه عبور'}),
        error_messages={'required': 'لطفا کلمه عبور را وارد نمایید.'},
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    def clean_confrim_password(self):
        password = self.cleaned_data.get('password')
        confrim_password = self.cleaned_data.get('confrim_password')

        if password == confrim_password:
            return password
        else:
            raise ValidationError('عدم سازگاری بین کلمه عبور با تکرار کلمه عبور وجود دارد.')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='پست الکترونیکی * ',
        widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}),
        error_messages={'required': 'لطفا پست الکترونیکی خود را خالی نگذارید.'}
    )
    password = forms.CharField(
        label='کلمه عبور * ',
        widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور'}),
        error_messages={'required': 'لطفا کلمه عبور را خالی نگذارید.'}
    )
    remember_me = forms.BooleanField(
        label='مرا بخاطر بسپار',
        widget=forms.CheckboxInput(attrs={'id': 'remember'}),
        required=False
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='پست الکترونیکی',
        widget=forms.EmailInput(attrs={'placeholder': 'آدرس ایمیل'}),
        error_messages={'required': 'لطغا آدرس ایمیل را خالی نگذارید.'}
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور'}),
        error_messages={'required': 'لطغا کلمه عبور را خالی نگذارید.'}
    )
    confrim_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'تکرار کلمه عبور'}),
        error_messages={'required': 'لطغا تکرار کلمه عبور را خالی نگذارید.'}
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    def clean_confrim_password(self):
        password = self.cleaned_data.get('password')
        confrim_password = self.cleaned_data.get('confrim_password')

        if password == confrim_password:
            return password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مقایرت دارند.')
