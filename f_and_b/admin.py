from django.contrib import admin
from .models import F_and_b
# Register your models here.
class F_and_bAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published', 'cooking_type', 'beverage_type', 'list_date'
    list_display_links = 'id', 'title'
    list_filter = 'cooking_type', 'beverage_type', 'list_date'
    list_editable = 'is_published',
    list_per_page = 30

admin.site.register(F_and_b, F_and_bAdmin)