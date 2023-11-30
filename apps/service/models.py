from django.db import models

from apps.site.models import ServiceIcon


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    icon = models.ForeignKey(to=ServiceIcon, on_delete=models.PROTECT, verbose_name='آیکن')
    description = models.CharField(max_length=400, verbose_name='توضیحات')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'سرویس ما'
        verbose_name_plural = 'سرویس های ما'

    def __str__(self):
        return self.title


class ServiceDetail(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    button_title = models.CharField(max_length=20, verbose_name='عنوان لینک')
    button_link = models.URLField(verbose_name='آدرس URL دکمه')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'جزییات سرویس ما'
        verbose_name_plural = 'جزییات سرویس های ما'

    def __str__(self):
        return self.title
