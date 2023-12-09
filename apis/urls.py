from django.urls import path, include

urlpatterns = [
    path("users/", include("apis.users.urls")),
    path("profiles/", include("apis.profiles.urls")),
    path("repositories/", include("apis.repositorys.urls")),
    path("event/", include("apis.events.urls")),
]
