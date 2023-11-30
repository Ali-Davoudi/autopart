from django.contrib import admin
from django.http import HttpRequest

from .models import Blog, BlogCategory, BlogTag, BlogComment


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date', 'author', 'is_active', 'is_delete']
    list_editable = ['is_active', 'is_delete']
    list_filter = ['is_active', 'is_delete']
    search_fields = ['title', 'description', 'short_description']

    def save_model(self, request: HttpRequest, obj: Blog, form, change: bool):
        if not change:
            obj.author = request.user
        return super(BlogAdmin, self).save_model(request, obj, form, change)


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'created_date', 'is_verify']
    list_editable = ['is_verify']


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(BlogComment, BlogCommentAdmin)
