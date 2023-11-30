from django.urls import path

from . import views

urlpatterns = [
    path('services/', views.ServiceTemplateView.as_view(), name='service')
]
