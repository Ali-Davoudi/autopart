from django.contrib import admin

from .models import Product, ProductCategory, ProductBrand, ProductGallery, ProductComment, ProductVisit


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'is_delete']
    list_editable = ['is_active']


class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'is_delete']
    list_editable = ['is_active']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'price', 'discount', 'discounted_price', 'sell_price', 'in_stock', 'is_active',
                    'is_delete']
    search_fields = ['title', 'brand']
    list_editable = ['is_active', 'discount', 'in_stock']


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_date', 'is_verify']
    list_editable = ['is_verify']
    search_fields = ['product__title', 'user__username', 'user__email', 'user__first_name', 'user__last_name']


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductVisit)
