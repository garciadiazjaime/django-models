from django.contrib import admin

from .models import Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "types", "permanently_closed", "gmaps_tries", "image"]


admin.site.register(Place, PlaceAdmin)
