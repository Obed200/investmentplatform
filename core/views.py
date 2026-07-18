from django.shortcuts import render

from investments.models import InvestmentPlan
from .models import Announcement, SiteSettings


def index(request):
    return render(
        request,
        'core/index.html',
        {
            "plans": InvestmentPlan.objects.filter(is_active=True),
            "site_settings": SiteSettings.load(),
            "announcements": Announcement.objects.filter(is_active=True)[:3],
        },
    )


def faq(request):
    return render(request, 'core/faq.html', {"site_settings": SiteSettings.load()})


def contact(request):
    return render(request, 'core/contact.html', {"site_settings": SiteSettings.load()})
