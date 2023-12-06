from django.urls import path
from apps.events import views

app_name = 'events'


urlpatterns = [
    path('create/', views.EventCreateView.as_view(), name='events-create'),
    path('', views.EventListView.as_view(), name='events-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='events-details'),


]


