from django.contrib import admin

from .models import BargainItem, BookCategory

admin.site.register(BargainItem)
admin.site.register(BookCategory)
# Register your models here.
