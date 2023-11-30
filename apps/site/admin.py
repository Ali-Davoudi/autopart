from django.contrib import admin

from .models import ContactInfo, ServiceIcon, PrivacyPolicy, SiteSetting, FooterCategoryTitle, FooterLink, SiteBanner


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['telephone', 'is_active']


class ServiceIconAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'footer_category', 'is_active']
    list_editable = ['is_active']


class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'top_position', 'url', 'is_active']
    list_editable = ['is_active']


admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(ServiceIcon, ServiceIconAdmin)
admin.site.register(PrivacyPolicy)
admin.site.register(SiteSetting)
admin.site.register(FooterLink, FooterLinkAdmin)
admin.site.register(FooterCategoryTitle)
admin.site.register(SiteBanner, SiteBannerAdmin)
