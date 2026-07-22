def admin_nav_badges(request):
    """Expose pending-approval counts to the admin sidebar on every page."""
    user = getattr(request, "user", None)
    if not (user and user.is_authenticated and user.is_staff):
        return {}
    from payments.models import Deposit, Withdrawal

    pending_deposits = Deposit.objects.filter(status=Deposit.PENDING).count()
    pending_withdrawals = Withdrawal.objects.filter(status=Withdrawal.PENDING).count()
    return {
        "nav_pending_deposits": pending_deposits,
        "nav_pending_withdrawals": pending_withdrawals,
        "nav_pending_total": pending_deposits + pending_withdrawals,
    }
