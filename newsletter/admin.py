from django.contrib import admin

from newsletter.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "created",
        "updated",
    ]
    search_fields = ["email"]


admin.site.register(Subscriber, SubscriberAdmin)
