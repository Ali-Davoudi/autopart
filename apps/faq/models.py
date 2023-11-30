from django.db import models
from django.db.models.signals import pre_save

from django.utils.crypto import get_random_string


class Faq(models.Model):
    question = models.CharField(max_length=450, verbose_name='سوال کاربر')
    answer = models.TextField(verbose_name='پاسخ به سوال کاربر')
    collapse = models.CharField(max_length=200, editable=False)
    heading = models.CharField(max_length=200, editable=False)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'

    def __str__(self):
        return self.question


def faq_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.collapse:
        instance.collapse = get_random_string(20)
    if not instance.heading:
        instance.heading = get_random_string(20)


pre_save.connect(faq_pre_save_receiver, sender=Faq)
