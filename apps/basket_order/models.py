from django.db import models
from django.utils import timezone

from jalali_date import datetime2jalali

from utils.validators import validate_discount

from apps.account.models import User
from apps.product.models import Product


class Coupon(models.Model):
    code = models.CharField(max_length=50, verbose_name='کد')
    discount = models.PositiveIntegerField(verbose_name='درصد تخفیف', validators=[validate_discount])
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'کوپن'
        verbose_name_plural = 'کوپن ها'

    def __str__(self):
        return self.code


class UserBasketOrder(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='پرداخت شده / پرداخت نشده')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ و زمان ایجاد')
    payment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='تاریخ و زمان پرداخت')
    coupon = models.ForeignKey(to=Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کوپن')

    class Meta:
        verbose_name = 'سبد خرید کاربر'
        verbose_name_plural = 'سبدهای خرید کاربران'

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.payment_date = timezone.now() if self.is_paid else None

        super().save(*args, **kwargs)

    def calculate_total_amount(self):
        total_amount = 0
        for order_detail in self.userbasketorderdetail_set.all():
            total_amount += order_detail.final_price

        if self.coupon and self.coupon.is_active:
            total_amount -= int(total_amount * (self.coupon.discount / 100))

        return total_amount

    def calculate_basket_amount(self):
        total_amount = 0
        for order_detail in self.userbasketorderdetail_set.all():
            total_amount += order_detail.final_price

        return total_amount

    def get_jalali_date(self):
        jalali_date = datetime2jalali(self.payment_date)
        month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                       'اسفند']
        month_index = jalali_date.month - 1
        month_name = month_names[month_index]
        return jalali_date.strftime('%d %s %Y') % month_name


class UserBasketOrderDetail(models.Model):
    user_basket_order = models.ForeignKey(to=UserBasketOrder, on_delete=models.PROTECT, verbose_name='سبد خرید کاربر')
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='محصول')
    product_count = models.PositiveIntegerField(verbose_name='تعداد محصول')
    final_price = models.PositiveBigIntegerField(verbose_name='قیمت نهایی محصول', null=True, blank=True)
    single_price = models.PositiveIntegerField(null=True)

    def save(self, *args, **kwargs):
        # If admin change the product price, This will not affect to the current user basket order detail and its factor
        if not self.single_price:
            self.single_price = self.product.sell_price

        if self.product_count:
            self.final_price = self.single_price * self.product_count

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'جزییات سبد خرید کاربر'
        verbose_name_plural = 'جزییات سبدهای خرید کاربران'

    def __str__(self):
        return str(self.user_basket_order)

    def get_coupon_price(self):
        if self.user_basket_order.coupon:
            return int(self.final_price * (self.user_basket_order.coupon.discount / 100))
        else:
            return self.final_price
