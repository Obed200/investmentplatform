from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import Profile
from core.models import Announcement, SiteSettings
from investments.models import Investment
from payments.models import Deposit, Withdrawal
from transactions.models import Transaction


@login_required
def user_dashboard(request):
    for investment in request.user.investments.filter(status=Investment.ACTIVE):
        investment.credit_due_earnings()
    today = timezone.localdate()
    context = {
        "wallet": request.user.wallet,
        "todays_earnings": request.user.transactions.filter(
            transaction_type=Transaction.EARNING,
            created_at__date=today,
        ).aggregate(total=Sum("amount"))["total"] or 0,
        "active_investment": request.user.investments.filter(status=Investment.ACTIVE).first(),
        "pending_deposit": request.user.deposits.filter(status=Deposit.PENDING).first(),
        "pending_withdrawal": request.user.withdrawals.filter(status=Withdrawal.PENDING).first(),
        "transactions": request.user.transactions.all()[:8],
        "notifications": request.user.notifications.all()[:5],
        "announcements": Announcement.objects.filter(is_active=True)[:3],
        "referral_count": Profile.objects.filter(referred_by=request.user).count(),
        "site_settings": SiteSettings.load(),
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@staff_member_required
def admin_dashboard(request):
    today = timezone.localdate()
    for investment in Investment.objects.filter(status=Investment.ACTIVE):
        investment.credit_due_earnings()
    context = {
        "total_users": Profile.objects.count(),
        "total_deposits": Deposit.objects.filter(status=Deposit.APPROVED).aggregate(total=Sum("amount"))["total"] or 0,
        "total_withdrawals": Withdrawal.objects.filter(status=Withdrawal.PAID).aggregate(total=Sum("amount"))["total"] or 0,
        "total_investments": Investment.objects.count(),
        "active_investments": Investment.objects.filter(status=Investment.ACTIVE).count(),
        "todays_earnings": Transaction.objects.filter(transaction_type=Transaction.EARNING, created_at__date=today).aggregate(total=Sum("amount"))["total"] or 0,
        "pending_deposits_count": Deposit.objects.filter(status=Deposit.PENDING).count(),
        "pending_withdrawals_count": Withdrawal.objects.filter(status=Withdrawal.PENDING).count(),
        "referral_bonuses": Transaction.objects.filter(transaction_type=Transaction.REFERRAL).aggregate(total=Sum("amount"))["total"] or 0,
        # Queues the admin acts on directly from this page
        "pending_deposit_list": Deposit.objects.filter(status=Deposit.PENDING).select_related("user", "user__profile", "plan"),
        "pending_withdrawal_list": Withdrawal.objects.filter(status=Withdrawal.PENDING).select_related("user", "user__profile"),
        "recent_users": Profile.objects.select_related("user").order_by("-created_at")[:8],
        "recent_transactions": Transaction.objects.select_related("user")[:10],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@staff_member_required
@require_POST
def approve_deposit(request, pk):
    deposit = get_object_or_404(Deposit, pk=pk)
    if deposit.status != Deposit.PENDING:
        messages.warning(request, "That deposit was already reviewed.")
    else:
        deposit.approve()
        if deposit.status == Deposit.APPROVED:
            messages.success(
                request,
                f"Approved {deposit.user.username}'s payment. Investment in {deposit.plan.name} is now active.",
            )
        else:
            messages.warning(request, f"Could not approve: {deposit.admin_note}")
    return redirect("dashboard:admin_dashboard")


@staff_member_required
@require_POST
def reject_deposit(request, pk):
    deposit = get_object_or_404(Deposit, pk=pk)
    note = request.POST.get("note", "").strip() or "Rejected by administrator."
    if deposit.status != Deposit.PENDING:
        messages.warning(request, "That deposit was already reviewed.")
    else:
        deposit.reject(note)
        messages.error(request, f"Rejected {deposit.user.username}'s payment.")
    return redirect("dashboard:admin_dashboard")


@staff_member_required
@require_POST
def approve_withdrawal(request, pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    if withdrawal.status != Withdrawal.PENDING:
        messages.warning(request, "That withdrawal was already reviewed.")
    else:
        withdrawal.approve()
        messages.success(request, f"Marked {withdrawal.user.username}'s withdrawal as paid.")
    return redirect("dashboard:admin_dashboard")


@staff_member_required
@require_POST
def reject_withdrawal(request, pk):
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    note = request.POST.get("note", "").strip() or "Rejected by administrator."
    if withdrawal.status != Withdrawal.PENDING:
        messages.warning(request, "That withdrawal was already reviewed.")
    else:
        withdrawal.reject(note)
        messages.error(request, f"Rejected {withdrawal.user.username}'s withdrawal.")
    return redirect("dashboard:admin_dashboard")
