from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Profile


@login_required
def referral_list(request):
    referrals = Profile.objects.filter(referred_by=request.user).select_related("user")
    return render(request, 'referrals/referral_list.html', {"referrals": referrals})
