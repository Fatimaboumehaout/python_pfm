from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description')
    ordering = ('start_date',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description')
        }),
        ('Période', {
            'fields': ('start_date', 'end_date')
        }),
    )
