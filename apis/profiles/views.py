from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from apis.users.token import JWTBlacklistedTokenCheck, CustomJWTAuthentication
from rest_framework.permissions import (
        IsAuthenticated, 
    )

from apps.core.utils import (
    ApiBaseView, 
    api_success, 
    api_error, 
    create_JWT_token, 
    html_mail_sender, 
)

from apps.users.models import UserOTP, Occupation, Academic
from django.contrib.auth import get_user_model
User = get_user_model()

from apis.profiles.serializers import (
    MemberProfileSerializer, 
    MentorProfileSerializer
)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [IsAuthenticated]
   
    def get(self, request, format=None):
        user = request.user

        if user.role == 'member':
            serializer = MemberProfileSerializer(user)
 
        elif user.role == 'mentor':
            serializer = MentorProfileSerializer(user)
 
        return api_success(serializer.data, status=200, message = 'Profile Data.')