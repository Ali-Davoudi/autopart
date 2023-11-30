from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from apps.api import views

urlpatterns = [
    path('auth-token/', obtain_auth_token),
    path('revoke-token/', views.RevokeToken.as_view()),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('products/', views.ProductList.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
