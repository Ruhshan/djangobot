from django.contrib import admin

# Register your models here.
from .models import Item, ItemCategory, PendingOrder, SubCategory

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'payload_code')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'payload_code')
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'postback_code')

admin.site.register(Item)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(PendingOrder)

