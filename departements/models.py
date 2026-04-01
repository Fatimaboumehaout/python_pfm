from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone

class Department(models.Model):
    """
    Modèle pour représenter les départements de l'établissement
    """
    # Champs de base
    name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="Nom du département (ex: Génie Informatique)"
    )
    code = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Code du département (ex: GI)"
    )
    description = models.TextField(
        blank=True,
        help_text="Description détaillée du département"
    )
    
    # Informations de contact
    hod_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Nom du responsable du département (Head of Department)"
    )
    hod_email = models.EmailField(blank=True)
    hod_phone = models.CharField(max_length=15, blank=True)
    
    # Localisation
    building = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Bâtiment du département"
    )
    floor = models.IntegerField(blank=True, null=True)
    room_number = models.CharField(max_length=50, blank=True)
    
    # Métadonnées
    founded_year = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Année de création du département"
    )
    budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Budget annuel alloué"
    )
    
    # Statut
    is_active = models.BooleanField(
        default=True,
        help_text="Indique si le département est actif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        db_table = 'departments'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_teachers_count(self):
        """Retourne le nombre d'enseignants du département"""
        return self.assignments.filter(is_current=True).count()
    
    def get_subjects_count(self):
        """Retourne le nombre de matières du département (à implémenter)"""
        return 0  # Temporaire jusqu'à la création du modèle Subject


class DepartmentAssignment(models.Model):
    """
    Modèle pour l'attribution des enseignants aux départements
    (table intermédiaire pour gérer les changements)
    """
    # Relation
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    teacher_id = models.CharField(max_length=100)  # ID du professeur
    teacher_name = models.CharField(max_length=255)
    teacher_email = models.EmailField(blank=True)
    
    # Détails du poste
    position = models.CharField(
        max_length=100,
        choices=[
            ('HOD', 'Head of Department'),
            ('SENIOR_LECTURER', 'Maître de Conférences'),
            ('LECTURER', 'Chargé de Cours'),
            ('ASSISTANT', 'Assistant'),
        ],
        default='LECTURER'
    )
    
    # Dates
    assigned_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('department', 'teacher_id', 'is_current')
        ordering = ['-assigned_date']
        verbose_name = "Attribution Enseignant"
        verbose_name_plural = "Attributions Enseignants"
    
    def __str__(self):
        return f"{self.teacher_name} -> {self.department.code}"
