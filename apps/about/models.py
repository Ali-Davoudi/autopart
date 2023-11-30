from django.db import models

from utils.validators import validate_rate


class ReasonChoice(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/about/reason-choice', verbose_name='تصویر', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'دلیل انتخاب شرکت'
        verbose_name_plural = 'دلایل انتخاب شرکت'

    def __str__(self):
        return self.title


class SpecializedField(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/about/specialized', verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'تخصص ما'
        verbose_name_plural = 'تخصص های ما'

    def __str__(self):
        return self.title


class CustomerComment(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام مشتری')
    major = models.CharField(max_length=100, verbose_name='تخصص')
    image = models.ImageField(upload_to='images/about/customer', verbose_name='تصویر مشتری')
    comment = models.TextField(verbose_name='نظر مشتری')
    rate = models.PositiveIntegerField(validators=[validate_rate], verbose_name='امتیاز کاربر به ما')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'نظر مشتری در مورد همکاری با ما'
        verbose_name_plural = 'نظرات مشتری در مورد همکاری با ما'

    def __str__(self):
        return self.name
