from django.contrib import admin

from .models import Category, Gift, PriceRange


class GiftAdmin(admin.ModelAdmin):
  list_display = ["title", "price", "category", "price_range"]

class CategoryAdmin(admin.ModelAdmin):
  list_display = ["name"]

class PriceRangeAdmin(admin.ModelAdmin):
  list_display = ["name"]

admin.site.register(PriceRange, PriceRangeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gift, GiftAdmin)
