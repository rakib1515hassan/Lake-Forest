from django.urls import path
from apps.events import views

app_name = 'events'


urlpatterns = [
    ## Event URL patterns
    path('create/', views.EventCreateView.as_view(), name='events-create'),
    path('', views.EventListView.as_view(), name='events-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='events-details'),


    ## Event Panel URL pattern
    path('panel-create/', views.EventPanelsCreateView.as_view(), name='events-panel-create'),
    path('panel/', views.EventPanelsListView.as_view(), name='events-panel-list'),


    ## Events Schedule URL pattern
    path('schedule-create/', views.EventsScheduleCreateView.as_view(), name='events-schedule-create'),
    path('schedule/', views.EventsScheduleListView.as_view(), name='events-schedule-list'),
    


]


