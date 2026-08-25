from django.contrib import admin
from .models import Merchant
# Register your models here.
class MerchantAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published', 'type', 'list_date'
    list_display_links = 'id', 'title'
    list_filter = 'type', 'list_date'
    list_editable = 'is_published',
    list_per_page = 30

admin.site.register(Merchant, MerchantAdmin)