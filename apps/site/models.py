from django.core.exceptions import ValidationError
from django.db import models

from ckeditor.fields import RichTextField

from utils.validators import validate_email


class SiteSetting(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    logo = models.ImageField(upload_to='images/site_logo', verbose_name='لوگوی شرکت')
    favicon = models.ImageField(upload_to='images/favicon', verbose_name='فوآیکن ( Favicon )', null=True, blank=True)
    instagram = models.CharField(max_length=150, verbose_name='آی دی اینستاگرام', null=True, blank=True)
    twitter = models.CharField(max_length=150, verbose_name='آی دی توییتر', null=True, blank=True)
    about_company = RichTextField(config_name='default', verbose_name='درباره شرکت')
    copyright = RichTextField(config_name='default', verbose_name='متن کپی رایت')

    class Meta:
        verbose_name = 'مشخصه کلی سایت'
        verbose_name_plural = 'مشخصات کلی سایت'

    def __str__(self):
        return self.title


class FooterCategoryTitle(models.Model):
    footer_category_title = models.CharField(max_length=80, verbose_name='عنوان دسته بندی')

    class Meta:
        verbose_name = 'عنوان دسته بندی لینک Footer سایت'
        verbose_name_plural = 'عنوان دسته بندی های لینک های Footer سایت'

    def __str__(self):
        return self.footer_category_title


class FooterLink(models.Model):
    title = models.CharField(max_length=90, verbose_name='عنوان')
    url = models.URLField(max_length=200, verbose_name='نشانی وب')
    footer_category = models.ForeignKey(to=FooterCategoryTitle, on_delete=models.PROTECT,
                                        verbose_name='عنوان دسته بندی')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'لینک Footer سایت'
        verbose_name_plural = 'لینک های Footer سایت'

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    address = models.TextField(verbose_name='آدرس')
    telephone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(validators=[validate_email], null=True, blank=True, verbose_name='ایمیل')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'اطلاع تماس'
        verbose_name_plural = 'اطلاعات تماس برای درج در سایت'

    def __str__(self):
        return self.telephone


class ServiceIcon(models.Model):
    icon = models.CharField(max_length=200, verbose_name='کلاس آیکن')
    title = models.CharField(max_length=100, verbose_name='عنوان آیکن')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'مدیریت آیکن بخش سرویس'
        verbose_name_plural = 'مدیریت آیکن های بخش سرویس'

    def __str__(self):
        return self.title


class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    header = RichTextField(config_name='default', verbose_name='عنوان سیاست حریم خصوصی')
    description = RichTextField(config_name='default', verbose_name='توضیحات')

    class Meta:
        verbose_name = 'سیاست حریم خصوصی'
        verbose_name_plural = 'سیاست های حریم خصوصی'

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزییات محصولات'
        home_page = 'home_page', 'صفحه اصلی'

    class TopSiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'بالای صفحه لیست محصولات'
        home_page = 'home_page', 'بالای صفحه اصلی'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(verbose_name='آدرس URL')
    image = models.ImageField(upload_to='images/site_banners', verbose_name='تصویر')
    position = models.CharField(max_length=100, choices=SiteBannerPosition.choices, verbose_name='جایگاه نمایشی',
                                null=True, blank=True)
    top_position = models.CharField(max_length=100, choices=TopSiteBannerPosition.choices,
                                    verbose_name='جایگاه نمایشی در بالای صفحه', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'

    def __str__(self):
        return self.title

    # Validate at least one required position for banner
    def clean(self):
        if not self.position and not self.top_position:
            raise ValidationError('حداقل باید یکی از جایگاه نمایشی بنر جهت درج در صفحه انتخاب گردد.')
        elif self.position and self.top_position:
            raise ValidationError('نمی توان هر دو جایگاه نمایشی را جهت درج بنر در صفحه انتخاب نمود.')
