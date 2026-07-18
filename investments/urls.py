from django.urls import path

from . import views

app_name = 'investments'

urlpatterns = [
    path('', views.plan_list, name='plan_list'),
    path('<int:pk>/', views.investment_detail, name='investment_detail'),
]
