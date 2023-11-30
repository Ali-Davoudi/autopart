from django.db.models import Count, Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from utils.convertors import group_list
from utils.http_services import get_client_ip

from .models import Product, ProductCategory, ProductBrand, ProductGallery, ProductComment, ProductVisit

from apps.basket_order.models import UserBasketOrder
from apps.site.models import SiteBanner
from apps.wishlist.models import UserWishList


class ProductListView(ListView):
    template_name = 'product/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 3
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['site_banners'] = SiteBanner.objects.filter(
            is_active=True,
            position__iexact=SiteBanner.SiteBannerPosition.product_list)
        context['top_site_banners'] = SiteBanner.objects.filter(
            is_active=True,
            top_position__iexact=SiteBanner.TopSiteBannerPosition.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')

        if category_name:
            query = query.filter(category__url_title__iexact=category_name, is_active=True, is_delete=False)

        if brand_name:
            query = query.filter(brand__url_title__iexact=brand_name, is_active=True, is_delete=False)

        return query.filter(is_active=True, is_delete=False)


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.annotate(
        product_count=Count('product', filter=Q(product__is_active=True, product__is_delete=False))).filter(
        is_active=True,
        is_delete=False)
    context = {'product_categories': product_categories}
    return render(request, 'product/product_categories.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(
        product_brand=Count('product', filter=Q(product__is_active=True, product__is_delete=False))).filter(
        is_active=True,
        is_delete=False)
    context = {'product_brands': product_brands}
    return render(request, 'product/product_brands.html', context)


class ProductDetailView(DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        loaded_product: Product = self.object
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id))
        galleries.insert(0, loaded_product)

        context['product_galleries'] = group_list(galleries, 4)
        context['related_products'] = Product.objects.filter(brand_id=loaded_product.brand_id, is_active=True,
                                                             is_delete=False).exclude(pk=loaded_product.id)[:8]

        context['comments'] = ProductComment.objects.filter(product_id=loaded_product.id, is_verify=True).order_by(
            '-created_date')
        context['comments_count'] = ProductComment.objects.filter(product_id=loaded_product.id, is_verify=True).count()

        if self.request.user.is_authenticated:
            try:
                current_user_basket_order = UserBasketOrder.objects.get(user_id=self.request.user.id, is_paid=False)
                current_user_basket_order_detail = current_user_basket_order.userbasketorderdetail_set.filter(
                    product_id=loaded_product.id, user_basket_order_id=current_user_basket_order.id).first()
            except UserBasketOrder.DoesNotExist:
                current_user_basket_order_detail = None

            current_user_wishlist, created = UserWishList.objects.prefetch_related(
                'userwishlistdetail_set').get_or_create(user_id=self.request.user.id)
            current_user_wishlist_detail = current_user_wishlist.userwishlistdetail_set.filter(
                product_id=loaded_product.id, user_wish_list_id=current_user_wishlist.id).first()

            context['current_user_basket_order_detail'] = current_user_basket_order_detail
            context['current_user_wishlist_detail'] = current_user_wishlist_detail

        # Most visited products
        user_ip = get_client_ip(self.request)
        user_id = self.request.user.id if self.request.user.is_authenticated else None

        has_visited_product = ProductVisit.objects.filter(product_id=loaded_product.id, ip__iexact=user_ip).exists()
        if not has_visited_product:
            visit_result = ProductVisit(
                user_id=user_id, product_id=loaded_product.id, ip=user_ip)
            visit_result.save()

        # Create next and previous product links
        next_product = Product.objects.filter(
            is_active=True,
            is_delete=False,
            id__gt=loaded_product.id
        ).first()
        previous_product = Product.objects.filter(
            is_active=True,
            is_delete=False,
            id__lt=loaded_product.id
        ).last()

        context['next_product'] = next_product
        context['previous_product'] = previous_product

        return context

    def get_queryset(self):
        query = super(ProductDetailView, self).get_queryset()
        return query.filter(is_active=True, is_delete=False)


class AddProductComment(View):
    def post(self, request: HttpRequest):
        comment_text = request.POST.get('comment_text')
        product_id = request.POST.get('product_id')

        if comment_text:
            comment = ProductComment(product_id=product_id, user_id=request.user.id, message=comment_text)
            comment.save()
            return JsonResponse({
                'status': 'ok',
                'title': 'عملیات موفقیت آمیز...',
                'text': 'دیدگاه شما با موفقیت ارسال شد و پس از تاًیید توسط ادمین در این صفحه منتشر خواهد شد.',
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'title': 'خطا...',
                'text': 'در صورت خالی بودن قسمت نظر؛ امکان ارسال آن وجود ندارد!',
                'icon': 'error'
            })

        context = {
            'comments': ProductComment.objects.filter(product_id=product_id, is_verify=True).order_by('-created_date'),
            'comments_count': ProductComment.objects.filter(product_id=product_id, is_verify=True).count()
        }
        return render(request, 'product/add_product_comment.html', context)


# Searching products
class SearchProductListView(ListView):
    template_name = 'product/product_list.html'  # Affected in header partial
    model = Product
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query is None:  # For empty search submiting then control the pagination and show all active products
            query = super(SearchProductListView, self).get_queryset()
            return query.filter(is_active=True, is_delete=False).order_by('-id')
        else:  # In this line query is filled (if query is filled, then have a lookup!)
            products = Product.objects.search(query).order_by('-id')
            return products
