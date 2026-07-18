from django.contrib import admin

from .models import Announcement, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "whatsapp_community_link", "telegram_community_link", "updated_at")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "message")
