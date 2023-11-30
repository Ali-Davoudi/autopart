from django.contrib import admin

from .models import Slider, SupportService, Sponser


class SliderAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'link', 'is_active']
    list_editable = ['is_active']


class SupportServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_title', 'is_active']
    list_editable = ['is_active']


class SponserAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active']
    list_editable = ['url', 'is_active']


admin.site.register(Slider, SliderAdmin)
admin.site.register(SupportService, SupportServiceAdmin)
admin.site.register(Sponser, SponserAdmin)
