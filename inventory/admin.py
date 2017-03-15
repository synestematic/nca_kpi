from django.contrib import admin

class ItemDisplayPrefs(admin.ModelAdmin):
    list_display = ['accountedFor', 'tag', 'device', 'history']


from .models import Item
admin.site.register(Item, ItemDisplayPrefs)
