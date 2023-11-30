from django.db import models


class Slider(models.Model):
    title = models.CharField(max_length=15, verbose_name='عنوان جزئی ( اختیاری )', null=True, blank=True)
    main_title = models.CharField(max_length=30, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر')
    link_title = models.CharField(max_length=15, verbose_name='عنوان لینک')
    link = models.URLField(max_length=150, verbose_name='لینک')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.main_title


class SupportService(models.Model):
    title = models.CharField(max_length=20, verbose_name='عنوان')
    sub_title = models.CharField(max_length=40, verbose_name='تعریف')
    image = models.ImageField(upload_to='images/support_services', verbose_name='تصویر')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=True)

    class Meta:
        verbose_name = 'سرویس پشتیبانی'
        verbose_name_plural = 'سرویس های پشتیبانی'

    def __str__(self):
        return self.title


class Sponser(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام شرکت/سازمان')
    image = models.ImageField(upload_to='images/sponsers', verbose_name='تصویر( لوگو ) شرکت')
    url = models.URLField(max_length=150, verbose_name='آدرس سایت شرکت ( اختیاری )', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسپانسر'
        verbose_name_plural = 'اسپانسرها'

    def __str__(self):
        return self.name
