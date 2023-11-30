from django.urls import path

from . import views

urlpatterns = [
    path('faq/', views.FaqTemplateView.as_view(), name='faq')
]
