from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import Occupation, Academic
from apps.events.models import EventsTeam

# from apps
User = get_user_model()
from rest_framework.exceptions import ValidationError


class UserOccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        exclude = ["updated_at", "created_at"]


class UserAcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        exclude = ["updated_at", "created_at"]


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "profile_img", "short_description"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "user_permissions", "groups", "updated_at", "last_login"]

        extra_kwargs = {
            "is_verified": {"read_only": True},
            "is_active": {"read_only": True},
            "is_admin": {"read_only": True},
            "is_superuser": {"read_only": True},
            "created_at": {"read_only": True},
            "role": {"read_only": True},
            "email": {"read_only": True},
            "name": {"required": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        role = self.context.get("role")
        if role == "mentor":
            representation["occupation"] = UserOccupationSerializer(
                instance.user_occupation.all(), many=True
            ).data
        elif role == "member":
            if my_team := instance.team_members.all():
                representation["my_mentor"] = UserSerializer(my_team.last().mentor).data
            try:
                representation["academic"] = UserAcademicSerializer(
                    instance.academic
                ).data
            except Exception:
                representation["academic"] = None
        return representation
