from django.contrib import admin

from .models import Investment, InvestmentPlan


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "daily_income", "duration_days", "total_revenue", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name",)


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "amount", "daily_income", "status", "start_date", "end_date", "total_earned")
    list_filter = ("status", "plan", "created_at")
    search_fields = ("user__username", "user__profile__full_name", "plan__name")
    actions = ("credit_due_earnings",)

    @admin.action(description="Credit due daily earnings")
    def credit_due_earnings(self, request, queryset):
        total = 0
        for investment in queryset:
            total += investment.credit_due_earnings()
        self.message_user(request, f"Credited {total} daily earning entries.")
