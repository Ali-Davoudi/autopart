from django.urls import path

from . import views

urlpatterns = [
    path('about-us/', views.AboutUsTemplateView.as_view(), name='about')
]
