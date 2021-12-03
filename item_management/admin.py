from django.contrib import admin

from .models import Item, BargainItem, BookCategory

admin.site.register(Item)
admin.site.register(BargainItem)
admin.site.register(BookCategory)
# Register your models here.
