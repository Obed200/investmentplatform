from django.contrib import admin

from .models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "current_balance", "withdrawable_balance", "daily_earnings", "referral_bonus", "updated_at")
    search_fields = ("user__username", "user__profile__full_name")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_type", "amount", "status", "created_at")
    list_filter = ("transaction_type", "status", "created_at")
    search_fields = ("user__username", "user__profile__full_name", "description")
