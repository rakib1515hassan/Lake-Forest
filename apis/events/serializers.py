from rest_framework import serializers

from apps.events.models import Event, EventsSchedule, EventsTeam, EventPanel
from apps.users.models import User


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "profile_img"]


class EventPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPanel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance.speaker.all())
        representation["speaker"] = SpeakerSerializer(
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
            representation["speaker"] = SpeakerSerializer(instance.speaker).data
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
            representation["mentor"] = SpeakerSerializer(instance.mentor).data
        member_list = []
        for i in instance.member.all():
            speaker = SpeakerSerializer(i).data
            member_list.append(speaker)
        representation["member"] = member_list
        representation["team_creator"] = SpeakerSerializer(instance.team_creator).data

        return representation


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

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
            speaker = SpeakerSerializer(i.speaker).data
            sp_list.append(speaker)
        representation["scheduled_speaker"] = sp_list

        representation["Registered"] = User.objects.count()
        representation["mentors"] = User.objects.filter(role="mentor").count()

        return representation
