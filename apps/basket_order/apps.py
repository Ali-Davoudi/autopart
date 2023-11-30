from django.apps import AppConfig


class BasketOrderModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.basket_order'
    verbose_name = 'ماژول سبدهای خرید'

    def ready(self):
        import apps.basket_order.signals
