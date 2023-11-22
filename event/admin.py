from django.contrib import admin

from .models import Location, Event, GMapsLocation


class GMapsLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "lat", "lng"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "gmaps_tries", "gmaps", "created", "updated"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "location", "gmaps", "created", "updated"]

    def gmaps(self, obj):
        return obj.location.gmaps


admin.site.register(GMapsLocation, GMapsLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
