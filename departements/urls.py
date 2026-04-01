from django.urls import path
from . import views

app_name = 'departements'

urlpatterns = [
    # ===== Routes spécifiques d'abord (avant les génériques) =====
    path(
        'add-department/',
        views.department_create,
        name='add_department'
    ),
    path(
        'api/departments/search/',
        views.department_api_search,
        name='api_search_departments'
    ),
    
    # ===== Routes avec ID (plus spécifiques) =====
    path(
        'departments/<int:dept_id>/update/',
        views.department_update,
        name='department_update'
    ),
    path(
        'departments/<int:dept_id>/delete/',
        views.department_delete,
        name='department_delete'
    ),
    path(
        'departments/<int:dept_id>/toggle-status/',
        views.department_toggle_status,
        name='department_toggle_status'
    ),
    path(
        'departments/<int:dept_id>/assign-teacher/',
        views.assign_teacher_to_department,
        name='assign_teacher'
    ),
    path(
        'departments/<int:dept_id>/assignments/<int:assignment_id>/remove/',
        views.remove_teacher_from_department,
        name='remove_assignment'
    ),
    path(
        'departments/<int:dept_id>/',
        views.department_detail,
        name='department_detail'
    ),
    
    # ===== Routes génériques (à la fin) =====
    path(
        'departments/create/',
        views.department_create,
        name='department_create'
    ),
    path(
        'departments/',
        views.department_list,
        name='department_list'
    ),
]
