from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.UserPanelDashboardView.as_view(), name='dashboard')
]
