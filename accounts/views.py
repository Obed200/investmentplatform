from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from core.models import SiteSettings

from .forms import PhoneLoginForm, ProfileForm, RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:user_dashboard")
    initial = {}
    ref = request.GET.get('ref') or request.GET.get('referral') or request.GET.get('r')
    if ref:
        initial['referral_code'] = ref.strip().upper()
    form = RegisterForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to Ribural Investments. Your account is ready.")
        return redirect("dashboard:user_dashboard")
    return render(request, 'accounts/register.html', {"form": form})


class RiburalLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = PhoneLoginForm


login_view = RiburalLoginView.as_view()
logout_view = LogoutView.as_view()


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        profile = form.save()
        request.user.username = profile.phone_number
        request.user.first_name = profile.full_name
        request.user.save(update_fields=["username", "first_name"])
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")
    return render(request, 'accounts/profile.html', {"form": form, "site_settings": SiteSettings.load()})
