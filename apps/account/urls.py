from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate-account/<active_code>/', views.AccountActivationView.as_view(), name='account_activation'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forget-password/', views.ForgetPasswwordView.as_view(), name='forget_password'),
    path('reset-password/<active_code>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('', include('social_django.urls', namespace='social'))
]
