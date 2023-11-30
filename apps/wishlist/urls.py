from django.urls import path

from . import views

urlpatterns = [
    path('my-wishlist/', views.user_wishlist, name='user_wishlist'),
    path('my-wishlist/add-to-wishlist/', views.AddToWishListView.as_view(), name='add_to_wishlist'),
    path('my-wishlist/remove-product-from-wishlist/', views.remove_favourite_product, name='remove_favourite_product')
]
