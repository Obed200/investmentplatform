from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Investment, InvestmentPlan


def plan_list(request):
    return render(request, 'investments/plan_list.html', {"plans": InvestmentPlan.objects.filter(is_active=True)})


@login_required
def investment_detail(request, pk):
    investment = get_object_or_404(Investment, pk=pk, user=request.user)
    investment.credit_due_earnings()
    return render(request, 'investments/investment_detail.html', {'investment': investment})
