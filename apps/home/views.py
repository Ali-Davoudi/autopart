from django.db.models import Count, Sum
from django.views.generic import TemplateView

from .models import Slider, SupportService, Sponser

from apps.product.models import ProductCategory, Product
from apps.site.models import SiteBanner


class HomeTemplateView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data()
        context['sliders'] = Slider.objects.filter(is_active=True)
        context['support_services'] = SupportService.objects.filter(is_active=True)

        categories = list(ProductCategory.objects.filter(is_active=True, is_delete=False))

        product_categories = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_set.filter(is_active=True, is_delete=False)),
            }
            product_categories.append(item)

        context['product_categories'] = product_categories

        context['sponsers'] = Sponser.objects.filter(is_active=True)

        context['most_visited_products'] = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')

        context['most_bought_products'] = Product.objects.filter(
            userbasketorderdetail__user_basket_order__is_paid=True, is_active=True, is_delete=False).annotate(
            order_count=Sum('userbasketorderdetail__product_count')).order_by('-order_count')

        context['banners'] = SiteBanner.objects.filter(
            is_active=True, position__iexact=SiteBanner.SiteBannerPosition.home_page)[:2]
        context['top_site_banners'] = SiteBanner.objects.filter(
            is_active=True, top_position__iexact=SiteBanner.TopSiteBannerPosition.home_page
        )

        context['special_discounts'] = Product.objects.filter(discount__gte=5, in_stock__gt=0, is_active=True,
                                                              is_delete=False)

        return context
