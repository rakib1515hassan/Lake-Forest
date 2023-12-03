from django.urls import path, include

urlpatterns = [
    path('users/', include('apis.users.urls')),
]