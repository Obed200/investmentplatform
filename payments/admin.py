from django.contrib import admin

from .models import Deposit, Withdrawal


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "amount", "status", "created_at", "reviewed_at")
    list_filter = ("status", "plan", "created_at")
    search_fields = ("user__username", "user__profile__full_name")
    readonly_fields = ("created_at", "reviewed_at")
    actions = ("approve_deposits", "reject_deposits")

    @admin.action(description="Approve selected deposits and activate investments")
    def approve_deposits(self, request, queryset):
        count = 0
        for deposit in queryset.filter(status=Deposit.PENDING):
            deposit.approve()
            count += 1
        self.message_user(request, f"Approved {count} deposits.")

    @admin.action(description="Reject selected deposits")
    def reject_deposits(self, request, queryset):
        count = 0
        for deposit in queryset.filter(status=Deposit.PENDING):
            deposit.reject("Rejected by administrator.")
            count += 1
        self.message_user(request, f"Rejected {count} deposits.")


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "phone_number", "status", "created_at", "reviewed_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "user__profile__full_name", "phone_number")
    readonly_fields = ("created_at", "reviewed_at")
    actions = ("approve_withdrawals", "reject_withdrawals")

    @admin.action(description="Mark selected withdrawals as paid")
    def approve_withdrawals(self, request, queryset):
        count = 0
        for withdrawal in queryset.filter(status=Withdrawal.PENDING):
            withdrawal.approve()
            count += 1
        self.message_user(request, f"Approved {count} withdrawals.")

    @admin.action(description="Reject selected withdrawals")
    def reject_withdrawals(self, request, queryset):
        count = 0
        for withdrawal in queryset.filter(status=Withdrawal.PENDING):
            withdrawal.reject("Rejected by administrator.")
            count += 1
        self.message_user(request, f"Rejected {count} withdrawals.")
