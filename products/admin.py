from django.contrib import admin
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published', 'type', 'origin', 'list_date'
    list_display_links = 'id', 'title'
    list_filter = 'type', 'list_date'
    list_editable = 'is_published',
    list_per_page = 30

admin.site.register(Product, ProductAdmin)