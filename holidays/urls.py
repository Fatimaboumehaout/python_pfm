from django.urls import path
from . import views

app_name = 'holidays'

urlpatterns = [
    path('', views.HolidayListView.as_view(), name='list'),
    path('calendar/', views.HolidayCalendarView.as_view(), name='calendar'),
    path('api/events/', views.holiday_events_api, name='events_api'),
    path('<int:pk>/', views.HolidayDetailView.as_view(), name='detail'),
    path('create/', views.HolidayCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.HolidayUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.HolidayDeleteView.as_view(), name='delete'),
]
