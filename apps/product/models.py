from django.db.models import Q
from django.urls import reverse
from django.db import models

from jalali_date import datetime2jalali

from utils.validators import validate_discount

from apps.account.models import User


class ProductManager(models.Manager):
    def search(self, query):
        lookup = (
                Q(title__icontains=query) | Q(short_description__icontains=query) |
                Q(description__icontains=query) | Q(production_country__icontains=query) |
                Q(brand__title__icontains=query) | Q(category__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, is_active=True, is_delete=False).distinct()


class ProductCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    url_title = models.CharField(max_length=120, verbose_name='عنوان در URL')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    class Meta:
        verbose_name = 'دسته بندی محصول'
        verbose_name_plural = 'دسته بندی های محصولات'

    def __str__(self):
        return self.title


class ProductBrand(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    url_title = models.CharField(max_length=120, verbose_name='عنوان در URL')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    class Meta:
        verbose_name = 'برند محصول'
        verbose_name_plural = 'برندهای محصولات'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    brand = models.ForeignKey(to=ProductBrand, on_delete=models.PROTECT, verbose_name='برند')
    category = models.ManyToManyField(to=ProductCategory, verbose_name='دسته بندی')
    short_description = models.TextField(verbose_name='توضیحات کوتاه', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات')
    production_date = models.PositiveBigIntegerField(verbose_name='سال ساخت')
    production_country = models.CharField(max_length=150, verbose_name='کشور سازنده')
    image = models.ImageField(upload_to='images/products', verbose_name='تصویر')
    price = models.PositiveBigIntegerField(verbose_name='قیمت محصول')
    discount = models.PositiveIntegerField(verbose_name='درصد اعمال تخفیف', default=0, blank=True,
                                           validators=[validate_discount])
    discounted_price = models.IntegerField(null=True)
    sell_price = models.IntegerField(null=True)
    in_stock = models.PositiveIntegerField(verbose_name='تعداد در انبار')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.title.replace(' ', '-')])

    # Discount calculations
    @property
    def discounted_price(self):
        if self.discount:
            return int(self.price * self.discount / 100)
        else:
            pass

    # Set a custom name for property that show the custom name in the admin panel
    discounted_price.fget.short_description = 'تخفیف'

    @property
    def sell_price(self):
        if self.discount:
            return int(self.price - self.discounted_price)
        else:
            return self.price

    sell_price.fget.short_description = 'قیمت فروش'


class ProductGallery(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_galleries', verbose_name='تصویر')

    class Meta:
        verbose_name = 'گالری تصویر محصول'
        verbose_name_plural = 'گالری تصاویر محصولات'

    def __str__(self):
        return self.product.title


class ProductComment(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='محصول')
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر')
    message = models.TextField(verbose_name='نظر کاربر')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    is_verify = models.BooleanField(verbose_name='تایید / عدم تایید توسط ادمین', default=False)

    class Meta:
        verbose_name = 'نظر کاربر در مورد محصول'
        verbose_name_plural = 'نظرات کاربران در مورد محصولات'

    def __str__(self):
        return str(self.user)

    def get_jalali_date(self):
        jalali_date = datetime2jalali(self.created_date)
        month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                       'اسفند']
        month_index = jalali_date.month - 1
        month_name = month_names[month_index]
        return jalali_date.strftime('%d %s %Y') % month_name


class ProductVisit(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='محصول')
    ip = models.CharField(max_length=100, verbose_name='آی پی کاربر')
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر', null=True, blank=True)

    class Meta:
        verbose_name = 'پر بازدیدترین محصول'
        verbose_name_plural = 'پر بازدیدترین محصولات'

    def __str__(self):
        return f"{self.product} - {self.ip}"
