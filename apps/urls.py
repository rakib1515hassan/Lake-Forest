from django.urls import path, include

urlpatterns = [
    path('', include('apps.dashboards.urls',  namespace='dashboards')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('repositorys/', include('apps.repositorys.urls', namespace='repositorys')),
]