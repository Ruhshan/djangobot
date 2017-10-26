from django.contrib import admin

# Register your models here.
from .models import Item, ItemCategory, PendingOrder

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'payload_code')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'postback_code')

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(PendingOrder)

