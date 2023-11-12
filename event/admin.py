from django.contrib import admin

from .models import Address, Location, Organizer, Event, GMapsLocation


class AddressAdmin(admin.ModelAdmin):
    list_display = ["street", "city", "state"]


class GMapsLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "lat", "lng"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "gmaps_tries", "gmaps"]


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ["name"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "location", "gmaps"]

    def gmaps(self, obj):
        return obj.location.gmaps


admin.site.register(Address, AddressAdmin)
admin.site.register(GMapsLocation, GMapsLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
