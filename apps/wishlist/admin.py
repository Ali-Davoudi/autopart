from django.contrib import admin

from .models import UserWishList, UserWishListDetail


class UserWishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'commit_datetime']


class UserWishListDetailAdmin(admin.ModelAdmin):
    list_display = ['user_wish_list', 'product']


admin.site.register(UserWishList, UserWishListAdmin)
admin.site.register(UserWishListDetail, UserWishListDetailAdmin)
