from django.urls import path, include

urlpatterns = [
    path('', include('apps.dashboards.urls',  namespace='dashboards')),
    path('users/', include('apps.users.urls', namespace='users')),
]