from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/deposit/<int:pk>/approve/', views.approve_deposit, name='approve_deposit'),
    path('admin/deposit/<int:pk>/reject/', views.reject_deposit, name='reject_deposit'),
    path('admin/withdrawal/<int:pk>/approve/', views.approve_withdrawal, name='approve_withdrawal'),
    path('admin/withdrawal/<int:pk>/reject/', views.reject_withdrawal, name='reject_withdrawal'),
]
