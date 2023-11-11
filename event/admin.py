from django.contrib import admin

from .models import Address, Location, Organizer, Event


class AddressAdmin(admin.ModelAdmin):
  list_display = ["street", "city", "state"]

class LocationAdmin(admin.ModelAdmin):
  list_display = ["name"]

class OrganizerAdmin(admin.ModelAdmin):
  list_display = ["name"]

class EventAdmin(admin.ModelAdmin):
  list_display = ["name", "start_date"]

admin.site.register(Address, AddressAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin

# Register your models here.
