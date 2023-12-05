from django.urls import path 

from apis.repositorys import views 

urlpatterns = [ 
    path('research-repository/<int:pk>/', views.ResearchRepositoryRetrieveView.as_view()), 
] 
