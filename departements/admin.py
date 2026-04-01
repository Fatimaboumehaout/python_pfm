from django.contrib import admin
from django.utils.html import format_html
from .models import Department, DepartmentAssignment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'hod_name', 'building', 
        'get_teachers_count', 'budget_display', 'status_badge', 'created_at'
    )
    list_filter = ('is_active', 'created_at', 'building')
    search_fields = ('name', 'code', 'hod_name', 'hod_email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations Générales', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Responsable', {
            'fields': ('hod_name', 'hod_email', 'hod_phone'),
            'classes': ('collapse',)
        }),
        ('Localisation', {
            'fields': ('building', 'floor', 'room_number'),
            'classes': ('collapse',)
        }),
        ('Budget & Année', {
            'fields': ('budget', 'founded_year'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_teachers_count(self, obj):
        """Affiche le nombre d'enseignants"""
        count = obj.get_teachers_count()
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 5px 10px; border-radius: 3px;">{}</span>',
            count
        )
    get_teachers_count.short_description = "Enseignants"
    
    def budget_display(self, obj):
        """Affiche le budget formaté"""
        if obj.budget:
            return format_html(
                '<span style="color: green; font-weight: bold;">{:,.2f} DH</span>',
                obj.budget
            )
        return "-"
    budget_display.short_description = "Budget"
    
    def status_badge(self, obj):
        """Badge pour le statut"""
        color = 'green' if obj.is_active else 'red'
        text = 'Actif' if obj.is_active else 'Inactif'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, text
        )
    status_badge.short_description = "Statut"


@admin.register(DepartmentAssignment)
class DepartmentAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'teacher_name', 'department', 'position', 'assigned_date', 
        'status_badge', 'assigned_duration'
    )
    list_filter = ('position', 'is_current', 'assigned_date', 'department')
    search_fields = ('teacher_name', 'teacher_id', 'teacher_email', 'department__name')
    readonly_fields = ('created_at', 'updated_at', 'assigned_duration')
    
    fieldsets = (
        ('Assignation', {
            'fields': ('department', 'position', 'is_current')
        }),
        ('Enseignant', {
            'fields': ('teacher_id', 'teacher_name', 'teacher_email')
        }),
        ('Dates', {
            'fields': ('assigned_date', 'end_date', 'assigned_duration')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Badge pour le statut de l'assignation"""
        color = 'green' if obj.is_current else 'gray'
        text = 'Actuelle' if obj.is_current else 'Passée'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, text
        )
    status_badge.short_description = "Statut"
    
    def assigned_duration(self, obj):
        """Affiche la durée de l'assignation"""
        from datetime import datetime
        
        end = obj.end_date or datetime.now().date()
        start = obj.assigned_date
        duration = (end - start).days
        
        years = duration // 365
        months = (duration % 365) // 30
        days = (duration % 365) % 30
        
        parts = []
        if years > 0:
            parts.append(f"{years}a")
        if months > 0:
            parts.append(f"{months}m")
        if days > 0 or not parts:
            parts.append(f"{days}j")
        
        return " ".join(parts)
    assigned_duration.short_description = "Durée"
