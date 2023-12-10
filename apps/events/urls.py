from django.urls import path
from apps.events import views

app_name = 'events'


urlpatterns = [
    ## Event URL patterns
    path('create/', views.EventCreateView.as_view(), name='events-create'),
    path('', views.EventListView.as_view(), name='events-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='events-details'),
    path('delete/<int:event_id>/', views.EventDeleteView.as_view(), name='event-delete'),
    path('update/<int:pk>/', views.EventUpdateView.as_view(), name='event-update'),


    ## Event Panels URL pattern
    path('panel-create/', views.EventPanelsCreateView.as_view(), name='events-panel-create'),
    path('panel-update/<int:pk>/', views.EventPanelsUpdateView.as_view(), name='events-panel-update'),
    path('panel-details/<int:pk>/', views.EventPanelsDetailView.as_view(), name='events-panel-details'),
    path('panel/', views.EventPanelsListView.as_view(), name='events-panel-list'),
    path('panel-delete/<int:pk>/', views.EventPanelsDeleteView.as_view(), name='events-panel-delete'),


    ## Events Schedules URL pattern
    path('schedule-create/', views.EventsScheduleCreateView.as_view(), name='events-schedule-create'),
    path('schedule/', views.EventsScheduleListView.as_view(), name='events-schedule-list'),
    path('schedule-details/<int:pk>/', views.EventsScheduleDetailView.as_view(), name='events-schedule-details'),
    path('schedule-delete/<int:pk>/', views.EventsScheduleDeleteView.as_view(), name='events-schedule-delete'),



    ## Events Teams URL pattern
    # path('schedule-create/', views.EventsScheduleCreateView.as_view(), name='events-schedule-create'),
    path('team/', views.EventsTeamListView.as_view(), name='events-team-list'),
    


]


