from django.contrib import admin
from .models import CustomerComment, SpecializedField, ReasonChoice


class ResonChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


class SpecializedFieldAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


class CustomerCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']


admin.site.register(ReasonChoice, ResonChoiceAdmin)
admin.site.register(SpecializedField, SpecializedFieldAdmin)
admin.site.register(CustomerComment, CustomerCommentAdmin)
