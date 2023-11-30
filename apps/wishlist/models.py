from django.db import models

from apps.account.models import User
from apps.product.models import Product


class UserWishList(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر')
    commit_datetime = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ثبت')

    class Meta:
        verbose_name = 'لیست علاقه مندی کاربر'
        verbose_name_plural = 'لیست علاقه مندی های کاربران'

    def __str__(self):
        return str(self.user)


class UserWishListDetail(models.Model):
    user_wish_list = models.ForeignKey(to=UserWishList, on_delete=models.PROTECT, verbose_name='کاربر')
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='محصول')

    class Meta:
        verbose_name = 'جزییات لیست علاقه مندی کاربر'
        verbose_name_plural = 'جزییات لیست علاقه مندی های کاربران'

    def __str__(self):
        return str(self.user_wish_list)
