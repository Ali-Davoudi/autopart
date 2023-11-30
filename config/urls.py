from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('auth/', include('apps.account.urls')),
    path('', include('apps.home.urls')),
    path('', include('apps.product.urls')),
    path('', include('apps.about.urls')),
    path('', include('apps.contact.urls')),
    path('', include('apps.service.urls')),
    path('', include('apps.faq.urls')),
    path('', include('apps.site.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.userpanel.urls')),
    path('', include('apps.basket_order.urls')),
    path('', include('apps.wishlist.urls')),
    path('', include('pwa.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
