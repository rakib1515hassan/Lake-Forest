from django.urls import path

from apis.repositorys import views

urlpatterns = [
    path("", views.ResearchRepositoryView.as_view()),
]
