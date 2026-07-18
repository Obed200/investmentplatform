from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "referral_code", "referred_by", "created_at")
    search_fields = ("full_name", "phone_number", "referral_code", "user__username")
    list_filter = ("created_at",)
