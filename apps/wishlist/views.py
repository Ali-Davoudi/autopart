from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import View

from .models import UserWishList, UserWishListDetail

from apps.product.models import Product


class AddToWishListView(View):
    def get(self, request: HttpRequest):
        product_id = int(request.GET.get('product_id'))

        if request.user.is_authenticated:
            product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()

            if product:
                current_user_wishlist, created = UserWishList.objects.get_or_create(user_id=request.user.id)
                current_user_wishlist_detail = current_user_wishlist.userwishlistdetail_set.filter(
                    user_wish_list_id=current_user_wishlist.id, product_id=product_id).first()

                if current_user_wishlist_detail:
                    current_user_wishlist_detail.save()

                else:
                    new_wishlist = UserWishListDetail(user_wish_list_id=current_user_wishlist.id, product_id=product_id)
                    new_wishlist.save()

                return JsonResponse({
                    'status': 'success',
                    'title': 'اعلان لیست علاقه مندی ها!',
                    'text': 'این محصول به لیست علاقه مندی های شما اضافه شد.',
                    'icon': 'success',
                    'show_bool_cancel_button': 'true',
                    'confrim_button_color': '#3085d6',
                    'cancel_button_color': '#d33',
                    'confrim_button_text': """<a href='/my-wishlist'>مشاهده</a>""",
                    'cancel_button_text': 'بازگشت'
                })

            else:
                return JsonResponse({
                    'status': 'product_not_found',
                    'title': 'اعلان لیست علاقه مندی ها!',
                    'text': 'محصول یافت نشد.',
                    'icon': 'error',
                    'show_bool_cancel_button': 'true',
                    'confrim_button_color': '#3085d6',
                    'confrim_button_text': 'آگاه شدم !',
                })

        else:
            return JsonResponse({
                'status': 'not_auth',
                'title': 'احراز هویت!',
                'text': 'برای ثبت محصول در لیست علاقه مندی ها، لازم است ابتدا وارد حساب کاربری خود شوید.',
                'icon': 'info',
                'show_bool_cancel_button': 'true',
                'confrim_button_color': '#3085d6',
                'cancel_button_color': '#d33',
                'confrim_button_text': """<a href='/login'>ورود به حساب کاربری</a>""",
                'cancel_button_text': 'بازگشت'
            })


@login_required
def user_wishlist(request: HttpRequest):
    current_user_wishlist, created = UserWishList.objects.prefetch_related('userwishlistdetail_set').get_or_create(
        user_id=request.user.id)

    context = {'current_user_wishlist': current_user_wishlist}

    return render(request, 'wishlist/wishlist.html', context)


@login_required
def site_header_wishlist_count(request: HttpRequest):
    current_user_wishlist, created = UserWishList.objects.prefetch_related('userwishlistdetail_set').get_or_create(
        user_id=request.user.id)

    context = {
        'user_wishlist_count': current_user_wishlist.userwishlistdetail_set.count()
    }
    return render(request, 'wishlist/site_header_wishlist_count.html', context)


@login_required
def remove_favourite_product(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))
    if detail_id is None:
        return JsonResponse({
            'status': 'invalid_id'
        })

    deleted_count, deleted_dict = UserWishListDetail.objects.filter(
        id=detail_id, user_wish_list__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'fav_product_not_found'
        })

    current_user_wishlist, created = UserWishList.objects.prefetch_related('userwishlistdetail_set').get_or_create(
        user_id=request.user.id)

    context = {'current_user_wishlist': current_user_wishlist}

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('wishlist/wishlist.html', context)
    })
