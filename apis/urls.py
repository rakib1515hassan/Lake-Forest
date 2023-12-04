from django.urls import path, include

urlpatterns = [
    path('users/', include('apis.users.urls')),
    path('profiles/', include('apis.profiles.urls')),
]