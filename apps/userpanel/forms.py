from django import forms
from django.core.exceptions import ValidationError

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from apps.account.models import User


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'email', 'mobile', 'avatar', 'address', 'birthdate']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'gender': 'جنسیت',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'پست الکترونیکی',
            'avatar': 'تصویر / آواتار',
            'address': 'آدرس',
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['birthdate'] = JalaliDateField(label='تاریخ تولد', widget=AdminJalaliDateWidget)
        self.fields['birthdate'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        accepted_serivces = ['gmail.com', 'yahoo.com', 'protonmail.com', 'pm.me', 'hotmail.com', 'outlook.com']
        _, service = email.split('@')
        if service.lower() not in accepted_serivces:
            raise ValidationError('آدرس ایمیل از سرویس های ایمیل مشهور یا امن مانند گوگل، یاهو و... نمی باشد.')
        return email


class ChangeUserPasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور جاری',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[]
    )
    confrim_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean_confrim_password(self):
        new_password = self.cleaned_data.get('new_password')
        confrim_password = self.cleaned_data.get('confrim_password')

        if new_password == confrim_password:
            return new_password

        raise forms.ValidationError('عدم هماهنگی بین کلمه عبور جدید با تکرار آن وجود دارد.')
