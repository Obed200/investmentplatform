from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from django.shortcuts import render

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
        "todays_earnings": Transaction.objects.filter(transaction_type=Transaction.EARNING, created_at__date=today).aggregate(total=Sum("amount"))["total"] or 0,
        "pending_deposits": Deposit.objects.filter(status=Deposit.PENDING).count(),
        "pending_withdrawals": Withdrawal.objects.filter(status=Withdrawal.PENDING).count(),
        "referral_bonuses": Transaction.objects.filter(transaction_type=Transaction.REFERRAL).aggregate(total=Sum("amount"))["total"] or 0,
        "active_investments": Investment.objects.filter(status=Investment.ACTIVE).count(),
        "recent_users": Profile.objects.order_by("-created_at")[:8],
        "recent_transactions": Transaction.objects.select_related("user")[:8],
        "deposit_days": Deposit.objects.values("created_at__date").annotate(total=Sum("amount")).order_by("-created_at__date")[:7],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
