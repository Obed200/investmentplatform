from django.urls import path

from . import views

app_name = 'referrals'

urlpatterns = [
    path('', views.referral_list, name='referral_list'),
]
