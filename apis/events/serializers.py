from rest_framework import serializers

from apps.events.models import Event, EventsSchedule, EventsTeam, EventPanel
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "profile_img", "short_description"]


class PanelScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsSchedule
        # fields = "__all__"
        exclude = ["updated_at", "created_at", "speaker", "event"]


class EventPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPanel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["panel_schedule"] = PanelScheduleSerializer(
            instance.panel_schedule.filter(panel=instance.id).first()
        ).data
        representation["speaker"] = UserSerializer(
            instance.speaker.all(), many=True
        ).data

        return representation


class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsSchedule
        # fields = "__all__"
        exclude = ["updated_at", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.speaker:
            representation["speaker"] = UserSerializer(instance.speaker).data
        if instance.panel:
            representation["panle"] = EventPanelSerializer(instance.panel).data

        return representation


class EventTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsTeam
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.mentor:
            representation["mentor"] = UserSerializer(instance.mentor).data
        member_list = []
        for i in instance.member.all():
            speaker = UserSerializer(i).data
            member_list.append(speaker)
        representation["member"] = member_list
        representation["team_creator"] = UserSerializer(instance.team_creator).data

        return representation


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        representation["entries"] = {
            "header_note": representation.pop("entries_header"),
            "white_paper_guidelines": representation.pop("paper_guidelines"),
            "presentation": representation.pop("presentation"),
        }
        representation["panels"] = EventPanelSerializer(
            instance.event_panel.all(), many=True
        ).data
        sp_list = []
        for i in instance.event_schedules.all():
            if i.speaker:
                speaker = EventScheduleSerializer(i).data
                sp_list.append(speaker)
        representation["scheduled_speaker"] = sp_list

        representation["Registered"] = User.objects.count()
        representation["mentors"] = User.objects.filter(role="mentor").count()
        representation["user"] = UserSerializer(request.user).data

        return representation
