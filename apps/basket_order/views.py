from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .models import UserBasketOrder, UserBasketOrderDetail, Coupon

from apps.product.models import Product


class AddProductToOrder(View):
    def get(self, request: HttpRequest):
        product_id = int(request.GET.get('product_id'))
        count = int(request.GET.get('count'))

        # Alert value, When user change product count [value] in inspect element
        if count < 1:
            return JsonResponse({
                'status': 'invalid_value',
                'title': 'خطا!',
                'text': 'مقدار وارد شده معتبر نمی باشد.',
                'icon': 'error',
                'confrim_button_color': '#006B1B',
                'confrim_button_text': 'آگاه شدم !'
            })

        if request.user.is_authenticated:
            product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()

            if product:
                # Alert In Stock, When user change product count [value] in inspect element
                if count > product.in_stock:
                    return JsonResponse({
                        'status': 'invalid_value',
                        'title': 'خطا!',
                        'text': 'این محصول با تعداد وارد شده در انبار موجود نمی باشد.',
                        'icon': 'error',
                        'confrim_button_color': '#006B1B',
                        'confrim_button_text': 'آگاه شدم !'
                    })
                # Get or create current user basket order
                current_user_basket_order, created = UserBasketOrder.objects.get_or_create(user_id=request.user.id,
                                                                                           is_paid=False)
                current_user_basket_order_detail = current_user_basket_order.userbasketorderdetail_set.filter(
                    product_id=product_id).first()

                if current_user_basket_order_detail:  # When current user basket order detail is available
                    current_user_basket_order_detail.product_count += count
                    product.in_stock -= count
                    product.save()
                    current_user_basket_order_detail.save()

                else:
                    new_order_detail = UserBasketOrderDetail(user_basket_order_id=current_user_basket_order.id,
                                                             product_id=product_id, product_count=count)
                    product.in_stock -= count
                    product.save()
                    new_order_detail.save()

                return JsonResponse({
                    'status': 'ok',
                    'title': 'عملیات موفقیت آمیز!',
                    'text': 'محصول به سبد خرید شما اضافه شد.',
                    'icon': 'success',
                    'confrim_button_color': '#006B1B',
                    'confrim_button_text': 'آگاه شدم !'
                })

            else:
                return JsonResponse({
                    'status': 'not_found',
                    'title': 'یافت نشد!',
                    'text': 'محصول یافت نشد.',
                    'icon': 'warning',
                    'confrim_button_color': '#006B1B',
                    'confrim_button_text': 'آگاه شدم !'
                })

        else:
            return JsonResponse({
                'status': 'not_auth',
                'title': 'احراز هویت!',
                'text': 'برای افزودن محصول به سبد خرید، لازم است ابتدا وارد حساب کاربری خود شوید.',
                'icon': 'info',
                'confrim_button_text': """<a href="/auth/login">ورود به حساب کاربری</a>""",
                'confrim_button_color': '#3085d6',
                'show_bool_cancel_button': 'true',
                'cancel_button_text': 'بازگشت'
            })


@login_required
def site_header_order_count(request: HttpRequest):
    try:
        current_user_basket_order = UserBasketOrder.objects.get(is_paid=False, user_id=request.user.id)
        user_basket_order_detail_count = current_user_basket_order.userbasketorderdetail_set.count()
    except UserBasketOrder.DoesNotExist:
        user_basket_order_detail_count = 0

    context = {
        'user_basket_order_detail_count': user_basket_order_detail_count
    }

    return render(request, 'basket_order/site_header_order_count.html', context)


@login_required
def site_header_mini_cart(request: HttpRequest):
    try:
        current_user_basket_order = UserBasketOrder.objects.get(is_paid=False, user_id=request.user.id)
        user_basket_order_sum = current_user_basket_order.calculate_total_amount()
    except UserBasketOrder.DoesNotExist:
        current_user_basket_order = None
        user_basket_order_sum = 0

    context = {
        'user_basket_order': current_user_basket_order,
        'user_basket_order_sum': user_basket_order_sum
    }

    return render(request, 'basket_order/site_header_mini_cart.html', context)


@login_required
def user_basket_order(request: HttpRequest):
    try:
        current_user_basket_order = UserBasketOrder.objects.prefetch_related(
            'userbasketorderdetail_set').get(user_id=request.user.id, is_paid=False)
    except UserBasketOrder.DoesNotExist:
        current_user_basket_order = None

    context = {
        'user_basket_order': current_user_basket_order
    }

    return render(request, 'basket_order/user_basket.html', context)


@login_required
def remove_an_order(request: HttpRequest):
    detail_id = int(request.GET.get('detail_id'))

    if detail_id is None:
        return JsonResponse({
            'status': 'invalid_order_detail_id'
        })

    user_basket_order_details = UserBasketOrderDetail.objects.filter(
        id=detail_id, user_basket_order__is_paid=False, user_basket_order__user_id=request.user.id)

    if not user_basket_order_details.exists():
        return JsonResponse({
            'status': 'order_detail_not_found'
        })

    # Iterate over all the order details being deleted and update the stock values of the corresponding products
    for user_basket_order_detail in user_basket_order_details:
        product = user_basket_order_detail.product
        product.in_stock += user_basket_order_detail.product_count
        product.save()

    deleted_count, deleted_dict = user_basket_order_details.delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'order_detail_not_found'
        })

    # After delete an order detail, we have to calculate total amount of the basket order
    current_user_basket_order, created = UserBasketOrder.objects.get_or_create(user_id=request.user.id, is_paid=False)
    user_basket_order_sum = current_user_basket_order.calculate_total_amount()

    context = {
        'user_basket_order': current_user_basket_order,
        'user_basket_order_sum': user_basket_order_sum
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('basket_order/user_basket.html', context)
    })


@method_decorator(login_required, name='dispatch')
class ApplyCouponView(View):
    def post(self, request):
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            user_basket_order = UserBasketOrder.objects.get(user=request.user, is_paid=False)

            if user_basket_order.coupon == coupon:
                response = {
                    'status': 'error',
                    'message': 'هم اکنون شما در حال استفاده از این کد تخفیف می باشید!'
                }
            else:
                user_basket_order.coupon = coupon
                user_basket_order.save()
                response = {
                    'status': 'success',
                    'message': 'کد تخفیف برای شما اعمال شد.'
                }
        except Coupon.DoesNotExist:
            response = {
                'status': 'error',
                'message': 'کد تخفیف معتبر نیست.'
            }

        return JsonResponse(response)
