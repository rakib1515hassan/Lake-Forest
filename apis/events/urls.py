from django.urls import path

from apis.events.views import EventView, EventScheduleView, EventTeamView

urlpatterns = [
    path("", EventView.as_view(), name="event"),
    path("schedule/", EventScheduleView.as_view(), name="event"),
    path("team/", EventTeamView.as_view(), name="team"),
]
