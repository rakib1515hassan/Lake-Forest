from apps.repositorys.models import (
        ResearchRepository,
        HelpfulResources,
        TaprootCauses,
        ResponseStrategies
    ) 
from apis.repositorys.serializers import (
        ResearchRepositorySerializer
    ) 
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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import generics, filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


class ResearchRepositoryRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
    queryset         = ResearchRepository.objects.all()
    serializer_class = ResearchRepositorySerializer

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['taproot_causes__title']

    def get(self, request, *args, **kwargs):
        instance   = self.get_object()
        serializer = self.get_serializer(instance)
        msg = "Research Repository Details."
        return api_success(serializer.data, status=200, message=msg)
