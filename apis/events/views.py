from apps.events.models import Event, EventsTeam, EventsSchedule
from apis.events.serializers import (
    EventsSerializer,
    EventScheduleSerializer,
    EventTeamSerializer,
)
from rest_framework.views import APIView
from django.db.models import Q
from apps.core.utils import (
    ApiBaseView,
    api_success,
    api_error,
    create_JWT_token,
    html_mail_sender,
)
from rest_framework import permissions


class EventView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventsSerializer
    queryset = Event.objects.all()

    def get(self, request, format=None):
        user = request.user
        event = self.queryset.last()
        if not event:
            return api_error({}, status=200, message="Event Doesn't Exist")
        event_serializer = self.serializer_class(event)
        return api_success(event_serializer.data, status=200, message="Event Data")


class EventScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventScheduleSerializer
    queryset = EventsSchedule.objects.all()

    def get(self, request, format=None):
        event = Event.objects.last()
        events_schedule = self.queryset.filter(event=event)
        if not events_schedule:
            return api_error({}, status=200, message="Events Schedule Exist")
        events_schedule_serializer = self.serializer_class(events_schedule, many=True)
        data = events_schedule_serializer.data
        deadlines = {
            "final_date": event.final_date,
            "submit_whitepaper_date": event.submit_whitepaper_date,
            "faculty_mentor_date": event.faculty_mentor_date,
            "select_topic_date": event.select_topic_date,
            "register_team_date": event.register_team_date,
        }
        data.append(deadlines)

        return api_success(data, status=200, message="Event Schedule Data")


class EventTeamView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventTeamSerializer
    queryset = EventsTeam.objects.all()

    def get(self, request, format=None):
        event = Event.objects.last()
        team = self.queryset.filter(event=event)
        serializer = self.serializer_class(team, many=True)
        return api_success(
            serializer.data, status=200, message="Event Team Get Successfully"
        )

    def post(self, request, format=None):
        current_user = request.user
        data = request.data.copy()
        event = Event.objects.last()
        data["event"] = event.id
        data["team_creator"] = current_user.id
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return api_error(
                {"errors": serializer.errors}, status=400, message="Doesn't Create"
            )
        serializer.save()
        return api_success(
            serializer.data, status=200, message="Event Team Successfully Created"
        )

    def patch(self, request, *args, **kwargs):
        data = request.data
        team_id = self.request.query_params.get("team_id")
        instance = self.queryset.get(id=team_id)
        serializer = self.serializer_class(instance, data=data)
        if serializer.is_valid():
            serializer.update(instance, data)
            return api_success(
                serializer.data, status=200, message="Event Team Update Successfully"
            )
