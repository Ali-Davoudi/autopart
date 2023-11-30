from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from utils.email_service import send_email
from utils.validators import validate_email, validate_rich_text


class Contact(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='نام کاربر')
    email = models.EmailField(validators=[validate_email], verbose_name='ایمیل کاربر')
    subject = models.CharField(max_length=350, null=True, blank=True, verbose_name='موضوع پیام')
    message = RichTextField(config_name='contact', verbose_name='متن پیام', validators=[validate_rich_text])
    response = RichTextField(config_name='default', verbose_name='متن پاسخ پیام توسط ادمین',
                             validators=[validate_rich_text], null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده / نشده')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ثبت')
    responsed_date = models.DateTimeField(verbose_name='تاریخ و زمان پاسخ', null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس های کاربران'

    def save(self, *args, **kwargs):
        if self.response:
            self.is_read_by_admin = True
            self.responsed_date = timezone.now()
            # Sending email response by Admin
            subject = f"اوتوپارت - پاسخ به تماس شما در تاریخ ارسالی {self.create_date.date()}"
            to = self.email
            context = {
                'response': self.response
            }
            template_name = 'core/email/contact_response.html'
            send_email(subject, to, context, template_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname
