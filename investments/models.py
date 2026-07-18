from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class InvestmentPlan(models.Model):
    name = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    daily_income = models.DecimalField(max_digits=12, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "amount"]

    @property
    def total_revenue(self):
        return self.daily_income * self.duration_days

    def __str__(self):
        return self.name


class Investment(models.Model):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACTIVE, "Active"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="investments")
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.PROTECT, related_name="investments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    daily_income = models.DecimalField(max_digits=12, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    last_credited_date = models.DateField(blank=True, null=True)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def days_remaining(self):
        if not self.end_date or self.status != self.ACTIVE:
            return 0
        return max((self.end_date - timezone.localdate()).days + 1, 0)

    def activate(self):
        today = timezone.localdate()
        self.status = self.ACTIVE
        self.start_date = today
        self.end_date = today + timedelta(days=self.duration_days - 1)
        self.save(update_fields=["status", "start_date", "end_date"])

    def credit_due_earnings(self):
        if self.status != self.ACTIVE or not self.start_date:
            return 0
        today = min(timezone.localdate(), self.end_date)
        if self.last_credited_date:
            next_date = self.last_credited_date + timedelta(days=1)
        else:
            next_date = self.start_date
        credited_days = 0
        while next_date <= today:
            self.user.wallet.credit(
                self.daily_income,
                "earning",
                f"Daily income from {self.plan.name} for {next_date}",
            )
            credited_days += 1
            self.total_earned += self.daily_income
            self.last_credited_date = next_date
            next_date += timedelta(days=1)
        if self.end_date and self.last_credited_date and self.last_credited_date >= self.end_date:
            self.status = self.COMPLETED
            from notifications.models import Notification

            Notification.objects.create(
                user=self.user,
                title="Investment Completed",
                message=f"{self.plan.name} has completed. You can invest again.",
            )
        if credited_days:
            self.save(update_fields=["total_earned", "last_credited_date", "status"])
        return credited_days

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
