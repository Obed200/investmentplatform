from django import forms

from core.models import Announcement, SiteSettings
from investments.models import Investment, InvestmentPlan


class InvestmentPlanForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        fields = ["name", "amount", "daily_income", "duration_days", "is_active", "sort_order"]


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ["plan", "amount", "daily_income", "duration_days", "status", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "is_active"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["whatsapp_community_link", "telegram_community_link", "contact_phone", "support_email"]
