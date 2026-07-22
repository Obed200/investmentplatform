from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),

    # Approval actions
    path('admin/deposit/<int:pk>/approve/', views.approve_deposit, name='approve_deposit'),
    path('admin/deposit/<int:pk>/reject/', views.reject_deposit, name='reject_deposit'),
    path('admin/withdrawal/<int:pk>/approve/', views.approve_withdrawal, name='approve_withdrawal'),
    path('admin/withdrawal/<int:pk>/reject/', views.reject_withdrawal, name='reject_withdrawal'),

    # Users
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/<int:pk>/', views.user_detail, name='user_detail'),
    path('admin/users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('admin/users/<int:pk>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
    path('admin/users/<int:pk>/toggle-staff/', views.user_toggle_staff, name='user_toggle_staff'),

    # Investment plans
    path('admin/plans/', views.manage_plans, name='manage_plans'),
    path('admin/plans/new/', views.plan_create, name='plan_create'),
    path('admin/plans/<int:pk>/edit/', views.plan_edit, name='plan_edit'),
    path('admin/plans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('admin/plans/<int:pk>/toggle/', views.plan_toggle, name='plan_toggle'),

    # Investments
    path('admin/investments/', views.manage_investments, name='manage_investments'),
    path('admin/investments/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('admin/investments/<int:pk>/credit/', views.investment_credit, name='investment_credit'),
    path('admin/investments/<int:pk>/cancel/', views.investment_cancel, name='investment_cancel'),

    # Transactions
    path('admin/transactions/', views.manage_transactions, name='manage_transactions'),

    # Community links
    path('admin/community/', views.manage_community, name='manage_community'),

    # Announcements
    path('admin/announcements/', views.manage_announcements, name='manage_announcements'),
    path('admin/announcements/new/', views.announcement_create, name='announcement_create'),
    path('admin/announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('admin/announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('admin/announcements/<int:pk>/toggle/', views.announcement_toggle, name='announcement_toggle'),
]
