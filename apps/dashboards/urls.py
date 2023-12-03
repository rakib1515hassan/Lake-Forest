from django.urls import path
from apps.dashboards import views

app_name = 'dashboards'


urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    path('', views.Home, name='home'),


]