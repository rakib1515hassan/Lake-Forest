from rest_framework import serializers 
from apps.repositorys.models import (
    ResearchRepository,
    HelpfulResources,
    TaprootCauses,
    ResponseStrategies
) 

class HelpfulResourcesSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = HelpfulResources 
        fields = '__all__' 

class TaprootCausesSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = TaprootCauses 
        fields = '__all__' 

class ResponseStrategiesSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ResponseStrategies 
        fields = '__all__' 


class ResearchRepositorySerializer(serializers.ModelSerializer): 
    helpful_resources   = HelpfulResourcesSerializer(many=True, read_only=True)
    taproot_causes      = TaprootCausesSerializer(many=True, read_only=True)
    response_strategies = ResponseStrategiesSerializer(many=True, read_only=True)

    class Meta: 
        model = ResearchRepository 
        fields = (
                'id', 'event', 'title', 'description', 'created_at', 'updated_at',
                'helpful_resources',
                'taproot_causes',
                'response_strategies',
            ) 
