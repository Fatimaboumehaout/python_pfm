from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from .models import Department, DepartmentAssignment
from .forms import DepartmentForm, DepartmentAssignmentForm

# ===== VUES POUR LES DÉPARTEMENTS =====

# @login_required(login_url='login')  # Commenté pour le développement
def department_list(request):
    """
    Liste tous les départements avec filtrage et recherche
    GET: Affiche la liste des départements
    """
    departments = Department.objects.all()
    
    # Recherche par nom ou code
    search_query = request.GET.get('search', '')
    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) | 
            Q(code__icontains=search_query) |
            Q(hod_name__icontains=search_query)
        )
    
    # Filtrage par statut
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'active':
        departments = departments.filter(is_active=True)
    elif status_filter == 'inactive':
        departments = departments.filter(is_active=False)
    
    # Ajouter le count des enseignants
    departments = departments.annotate(
        teachers_count=Count('assignments', distinct=True)
    )
    
    context = {
        'departments': departments,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': Department.objects.count(),
        'active_count': Department.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'departements/department_list.html', context)


# @login_required(login_url='login')  # Commenté pour le développement
def department_detail(request, dept_id):
    """
    Affiche les détails d'un département avec ses enseignants
    """
    try:
        department = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        return render(request, 'departements/department_detail.html', {
            'error': f'Département avec ID {dept_id} non trouvé',
            'department': None
        })
    
    # Récupérer les enseignants actuels du département
    current_assignments = department.assignments.filter(is_current=True)
    
    # Historique des attributions
    assignment_history = department.assignments.filter(is_current=False).order_by('-end_date')
    
    context = {
        'department': department,
        'current_assignments': current_assignments,
        'assignment_history': assignment_history,
        'teachers_count': current_assignments.count(),
    }
    
    return render(request, 'departements/department_detail.html', context)


# @login_required(login_url='login')  # Commenté pour le développement
@require_http_methods(["GET", "POST"])
def department_create(request):
    """
    Crée un nouveau département
    GET: Affiche le formulaire
    POST: Traite la soumission du formulaire
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(
                request, 
                f"Département '{department.name}' créé avec succès."
            )
            return redirect('departements:department_detail', department.pk)
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifiez les champs.")
    else:
        form = DepartmentForm()
    
    context = {'form': form, 'action': 'Créer'}
    return render(request, 'departements/department_form.html', context)


# @login_required(login_url='login')  # Commenté pour le développement
@require_http_methods(["GET", "POST"])
def department_update(request, dept_id):
    """
    Met à jour un département existant
    GET: Affiche le formulaire pré-rempli
    POST: Traite la modification
    """
    department = get_object_or_404(Department, id=dept_id)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                f"Département '{department.name}' mis à jour avec succès."
            )
            return redirect('departements:department_detail', department.pk)
        else:
            messages.error(request, "Erreur dans la mise à jour.")
    else:
        form = DepartmentForm(instance=department)
    
    context = {'form': form, 'action': 'Modifier', 'department': department}
    return render(request, 'departements/department_form.html', context)


# @login_required(login_url='login')  # Commenté pour le développement
@require_http_methods(["POST"])
def department_delete(request, dept_id):
    """
    Supprime un département
    POST uniquement pour la sécurité
    """
    department = get_object_or_404(Department, id=dept_id)
    dept_name = department.name
    
    try:
        department.delete()
        messages.success(
            request, 
            f"Département '{dept_name}' supprimé avec succès."
        )
    except Exception as e:
        messages.error(
            request, 
            f"Erreur lors de la suppression : {str(e)}"
        )
    
    return redirect('departements:department_list')


# @login_required(login_url='login')  # Commenté pour le développement
@require_http_methods(["POST"])
def department_toggle_status(request, dept_id):
    """
    Bascule le statut actif/inactif d'un département
    """
    department = get_object_or_404(Department, id=dept_id)
    department.is_active = not department.is_active
    department.save()
    
    status = "activé" if department.is_active else "désactivé"
    messages.success(request, f"Département {status}.")
    
    return redirect('departements:department_detail', department.pk)


# ===== VUES POUR L'ATTRIBUTION DES ENSEIGNANTS =====

# @login_required(login_url='login')  # Commenté pour le développement
def assign_teacher_to_department(request, dept_id):
    """
    Assigne un enseignant à un département
    GET: Affiche le formulaire
    POST: Traite l'assignation
    """
    department = get_object_or_404(Department, id=dept_id)
    
    if request.method == 'POST':
        form = DepartmentAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.department = department
            
            # Vérifier s'il existe une attribution actuelle
            existing = DepartmentAssignment.objects.filter(
                department=department,
                teacher_id=form.cleaned_data.get('teacher_id'),
                is_current=True
            ).first()
            
            if existing:
                messages.warning(
                    request, 
                    "Cet enseignant est déjà assigné à ce département."
                )
                return redirect('departements:department_detail', department.pk)
            
            assignment.save()
            messages.success(
                request, 
                f"Enseignant '{assignment.teacher_name}' assigné avec succès."
            )
            return redirect('departements:department_detail', department.pk)
    else:
        form = DepartmentAssignmentForm()
    
    context = {
        'form': form,
        'department': department,
        'action': 'Assigner'
    }
    return render(request, 'departements/assignment_form.html', context)


# @login_required(login_url='login')  # Commenté pour le développement
@require_http_methods(["POST"])
def remove_teacher_from_department(request, dept_id, assignment_id):
    """
    Retire un enseignant d'un département
    """
    department = get_object_or_404(Department, id=dept_id)
    assignment = get_object_or_404(
        DepartmentAssignment, 
        id=assignment_id, 
        department=department
    )
    
    teacher_name = assignment.teacher_name
    
    # Marquer comme non-actif au lieu de supprimer
    assignment.is_current = False
    assignment.end_date = timezone.now().date()
    assignment.save()
    
    messages.success(
        request, 
        f"Enseignant '{teacher_name}' retiré du département."
    )
    
    return redirect('departements:department_detail', department.pk)


# @login_required(login_url='login')  # Commenté pour le développement
def department_api_search(request):
    """
    API pour la recherche de départements (utilisée par autocomplete)
    Retourne JSON
    """
    query = request.GET.get('q', '')
    departments = Department.objects.filter(
        Q(name__icontains=query) | Q(code__icontains=query),
        is_active=True
    )[:10]
    
    data = [
        {'id': d.id, 'name': d.name, 'code': d.code}
        for d in departments
    ]
    
    return JsonResponse({'results': data})
