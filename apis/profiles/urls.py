from django.urls import path 

from apis.profiles import views

urlpatterns = [ 
    path('profile/', views.UserProfileView.as_view()), 

] 