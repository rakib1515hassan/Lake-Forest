from apps.repositorys.models import (
    ResearchRepository,
    HelpfulResources,
    TaprootCauses,
    ResponseStrategies,
)
from apis.repositorys.serializers import ResearchRepositorySerializer
from apps.core.utils import (
    ApiBaseView,
    api_success,
    api_error,
    create_JWT_token,
    html_mail_sender,
    sms_sender,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q
from apps.events.models import Event


class ResearchRepositoryView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = ResearchRepository.objects.all()
    serializer_class = ResearchRepositorySerializer

    def get(self, request, *args, **kwargs):
        event = Event.objects.last()
        instance = self.queryset.get(event=event)
        serializer = self.serializer_class(instance)
        return api_success(
            serializer.data, status=200, message="Successfully Research Repository"
        )
