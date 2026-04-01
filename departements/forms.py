from django import forms
from django.core.exceptions import ValidationError
from .models import Department, DepartmentAssignment
from datetime import datetime


class DepartmentForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier les départements
    """
    class Meta:
        model = Department
        fields = [
            'name', 'code', 'description', 'hod_name', 'hod_email', 'hod_phone',
            'building', 'floor', 'room_number', 'founded_year', 'budget', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Génie Informatique',
                'required': True
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: GI',
                'maxlength': '50',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du département',
                'rows': 4
            }),
            'hod_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du responsable',
            }),
            'hod_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemple.com',
            }),
            'hod_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+212 6XX XXX XXX',
            }),
            'building': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bâtiment A',
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': '0'
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 201',
            }),
            'founded_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024',
                'min': '1900',
                'max': str(datetime.now().year)
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50000.00',
                'step': '0.01'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': 'Nom du Département',
            'code': 'Code',
            'description': 'Description',
            'hod_name': 'Responsable (HOD)',
            'hod_email': 'Email du Responsable',
            'hod_phone': 'Téléphone du Responsable',
            'building': 'Bâtiment',
            'floor': 'Étage',
            'room_number': 'Numéro de Bureau',
            'founded_year': 'Année de Création',
            'budget': 'Budget (DH)',
            'is_active': 'Actif',
        }
    
    def clean_name(self):
        """Valider que le nom n'existe pas déjà"""
        name = self.cleaned_data.get('name')
        if name:
            # Si c'est une modification, exclure l'objet actuel
            qs = Department.objects.filter(name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Un département avec ce nom existe déjà.")
        return name
    
    def clean_code(self):
        """Valider que le code n'existe pas déjà"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
            qs = Department.objects.filter(code__iexact=code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Un département avec ce code existe déjà.")
        return code
    
    def clean_founded_year(self):
        """Valider que l'année de création est valide"""
        year = self.cleaned_data.get('founded_year')
        if year:
            current_year = datetime.now().year
            if year > current_year:
                raise ValidationError("L'année de création ne peut pas être dans le futur.")
            if year < 1900:
                raise ValidationError("L'année de création doit être après 1900.")
        return year
    
    def clean_budget(self):
        """Valider que le budget est positif"""
        budget = self.cleaned_data.get('budget')
        if budget and budget < 0:
            raise ValidationError("Le budget doit être positif.")
        return budget


class DepartmentAssignmentForm(forms.ModelForm):
    """
    Formulaire pour assigner des enseignants aux départements
    """
    class Meta:
        model = DepartmentAssignment
        fields = [
            'teacher_id', 'teacher_name', 'teacher_email', 'position', 'assigned_date'
        ]
        widgets = {
            'teacher_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID de l\'enseignant',
                'required': True
            }),
            'teacher_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet de l\'enseignant',
                'required': True
            }),
            'teacher_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@universite.ma',
            }),
            'position': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'assigned_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
        }
        labels = {
            'teacher_id': 'ID Enseignant',
            'teacher_name': 'Nom de l\'Enseignant',
            'teacher_email': 'Email',
            'position': 'Poste',
            'assigned_date': 'Date d\'Assignation',
        }
    
    def clean(self):
        """Validations transversales"""
        cleaned_data = super().clean()
        teacher_id = cleaned_data.get('teacher_id')
        assigned_date = cleaned_data.get('assigned_date')
        
        # Vérifier que la date d'assignation n'est pas dans le futur
        if assigned_date and assigned_date > datetime.now().date():
            raise ValidationError("La date d'assignation ne peut pas être dans le futur.")
        
        return cleaned_data
    
    def clean_teacher_id(self):
        """Valider l'ID enseignant"""
        teacher_id = self.cleaned_data.get('teacher_id')
        if teacher_id and len(teacher_id) < 3:
            raise ValidationError("L'ID enseignant doit avoir au minimum 3 caractères.")
        return teacher_id
