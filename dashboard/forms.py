from django import forms

from core.models import Announcement, SiteSettings
from investments.models import InvestmentPlan


class InvestmentPlanForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        fields = ["name", "amount", "daily_income", "duration_days", "is_active", "sort_order"]


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "is_active"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["whatsapp_community_link", "telegram_community_link", "contact_phone", "support_email"]
