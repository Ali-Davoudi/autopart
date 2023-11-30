from django.apps import AppConfig


class BlogModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
    verbose_name = 'ماژول مقالات'
