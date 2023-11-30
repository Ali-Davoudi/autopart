from django.db import models
from django.db.models import Q
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from jalali_date import date2jalali, datetime2jalali

from apps.account.models import User


class BlogManager(models.Manager):
    def search(self, query):
        lookup = (Q(title__icontains=query) |
                  Q(short_description__icontains=query) |
                  Q(description__icontains=query) |
                  Q(category__title__icontains=query) |
                  Q(tag__title__icontains=query)
                  )
        return self.get_queryset().filter(lookup, is_active=True, is_delete=False).distinct()


class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=250, verbose_name='عنوان در URL')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقالات'

    def __str__(self):
        return f'{self.title} - {self.url_title}'


class BlogTag(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=250, verbose_name='عنوان در URL')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برچسب مقاله'
        verbose_name_plural = 'برچسب های مقالات'

    def __str__(self):
        return f'{self.title} - {self.url_title}'


class Blog(models.Model):
    title = models.CharField(max_length=350, verbose_name='عنوان')
    short_description = RichTextUploadingField(config_name='default', verbose_name='توضیحات کوتاه')
    description = RichTextUploadingField(config_name='default', verbose_name='متن اصلی مقاله')
    category = models.ForeignKey(to=BlogCategory, on_delete=models.PROTECT, verbose_name='دسته بندی')
    tag = models.ManyToManyField(to=BlogTag, verbose_name='برچسب (تگ)')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر')
    author = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='نویسنده', null=True, blank=True,
                               editable=False)
    created_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    objects = BlogManager()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.id, self.title.replace(' ', '-')])

    def get_jalali_date(self):
        jalali_date = datetime2jalali(self.created_date)
        month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                       'اسفند']
        month_index = jalali_date.month - 1
        month_name = month_names[month_index]
        return jalali_date.strftime('%d %s %Y') % month_name


class BlogComment(models.Model):
    article = models.ForeignKey(to=Blog, on_delete=models.PROTECT, verbose_name='مقاله')
    parent = models.ForeignKey(to='BlogComment', null=True, blank=True, on_delete=models.PROTECT, verbose_name='والد')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر')
    message = models.TextField(verbose_name='متن نظر')
    is_verify = models.BooleanField(verbose_name='تایید / عدم تایید توسط ادمین', default=False)

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقالات'

    def __str__(self):
        return str(self.user)

    def get_jalali_date(self):
        jalali_date = datetime2jalali(self.created_date)
        month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                       'اسفند']
        month_index = jalali_date.month - 1
        month_name = month_names[month_index]
        return jalali_date.strftime('%d %s %Y') % month_name

    def get_jalali_time(self):
        return datetime2jalali(self.created_date).strftime('%H:%M')
