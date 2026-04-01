from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Holiday
from .forms import HolidayForm

class HolidayListView(LoginRequiredMixin, ListView):
    model = Holiday
    template_name = 'holidays/holiday_list.html'
    context_object_name = 'holidays'
    paginate_by = 10

class HolidayDetailView(LoginRequiredMixin, DetailView):
    model = Holiday
    template_name = 'holidays/holiday_detail.html'
    context_object_name = 'holiday'

class HolidayCreateView(LoginRequiredMixin, CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holidays/holiday_form.html'
    success_url = reverse_lazy('holidays:list')

    def form_valid(self, form):
        messages.success(self.request, 'Vacance créée avec succès!')
        return super().form_valid(form)

class HolidayUpdateView(LoginRequiredMixin, UpdateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holidays/holiday_form.html'
    success_url = reverse_lazy('holidays:list')

    def form_valid(self, form):
        messages.success(self.request, 'Vacance mise à jour avec succès!')
        return super().form_valid(form)

class HolidayDeleteView(LoginRequiredMixin, DeleteView):
    model = Holiday
    template_name = 'holidays/holiday_confirm_delete.html'
    success_url = reverse_lazy('holidays:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Vacance supprimée avec succès!')
        return super().delete(request, *args, **kwargs)

class HolidayCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'holidays/holiday_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['holidays'] = Holiday.objects.all()
        return context

def holiday_events_api(request):
    """API endpoint pour FullCalendar"""
    holidays = Holiday.objects.all()
    events = []
    
    for holiday in holidays:
        events.append({
            'title': holiday.name,
            'start': holiday.start_date.isoformat(),
            'end': holiday.end_date.isoformat(),
            'description': holiday.description or '',
            'url': f'/holidays/{holiday.pk}/',
            'backgroundColor': '#ff6b6b',
            'borderColor': '#ff5252',
            'textColor': '#ffffff'
        })
    
    return JsonResponse(events, safe=False)
