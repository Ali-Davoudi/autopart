from django.urls import path

from . import views

urlpatterns = [
    path('my-basket-order/add-to-order/', views.AddProductToOrder.as_view(), name='add_to_order'),
    path('my-basket-order/', views.user_basket_order, name='user_basket_order'),
    path('my-basket-order/remove-order/', views.remove_an_order, name='remove_order'),
    path('my-basket-order/apply-coupon/', views.ApplyCouponView.as_view(), name='apply_coupon'),
]
