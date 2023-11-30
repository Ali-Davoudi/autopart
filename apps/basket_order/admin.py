from django.contrib import admin

from .models import UserBasketOrder, UserBasketOrderDetail, Coupon


class UserBasketOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'payment_date', 'is_paid']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__email']


class UserBasketOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['user_basket_order', 'product', 'product_count', 'final_price']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
    list_per_page = 10
    search_fields = ['code']


admin.site.register(UserBasketOrder, UserBasketOrderAdmin)
admin.site.register(UserBasketOrderDetail, UserBasketOrderDetailAdmin)
admin.site.register(Coupon, CouponAdmin)
