from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('deposit/', views.deposit_create, name='deposit_create'),
    path('withdrawal/', views.withdrawal_create, name='withdrawal_create'),
]
