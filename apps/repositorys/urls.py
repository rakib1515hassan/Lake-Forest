from django.urls import path
from apps.repositorys import views

app_name = 'repositorys'


urlpatterns = [
    path('create/', views.EventRepositoryCreateView.as_view(), name='events-repository-create'),
    # path('<int:pk>/', views.EventDetailView.as_view(), name='events-details'),


]