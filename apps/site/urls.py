from django.urls import path

from . import views

urlpatterns = [
    path('privacy-policy/', views.PrivacyPolicyTemplateView.as_view(), name='privacy_policy')
]
