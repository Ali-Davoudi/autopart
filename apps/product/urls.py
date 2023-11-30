from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/category/<cat>', views.ProductListView.as_view(), name='product_categories'),
    path('products/brand/<brand>', views.ProductListView.as_view(), name='product_brands'),
    path('products/<pk>/<name>', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add-product-comment', views.AddProductComment.as_view(), name='add_product_comment'),
    path('products/all', views.SearchProductListView.as_view(), name='search_products')
]
