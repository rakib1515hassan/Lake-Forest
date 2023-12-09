from rest_framework import serializers
from apps.repositorys.models import (
    ResearchRepository,
    HelpfulResources,
    TaprootCauses,
    ResponseStrategies,
    ImpactOnSociety,
)


class HelpfulResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpfulResources
        fields = "__all__"


class TaprootCausesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaprootCauses
        fields = "__all__"


class ImpactOnSocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactOnSociety
        fields = "__all__"


class ResponseStrategiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseStrategies
        fields = "__all__"


class ResearchRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchRepository
        exclude = ["updated_at", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["information"] = {
            "title": representation.pop("title"),
            "description": representation.pop("description"),
            "helpful_resources": HelpfulResourcesSerializer(
                instance.helpful_resources, many=True
            ).data,
        }
        representation["taproot_causes"] = TaprootCausesSerializer(
            instance.taproot_causes, many=True
        ).data
        representation["response_strategies"] = TaprootCausesSerializer(
            instance.response_strategies, many=True
        ).data
        representation["impact_on_society"] = TaprootCausesSerializer(
            instance.impact_on_society, many=True
        ).data

        return representation
