from datetime import datetime, timedelta, timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import random
from django.db.models import Q

from django.template.loader import render_to_string
from apps.core.utils import html_mail_sender, sms_sender
from django.core.mail import EmailMultiAlternatives
from apps.users.models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(
            write_only=True, 
            required=True, 
            validators=[validate_password], 
            style={'input_type':'password'}
        )
    password2 = serializers.CharField(
            write_only=True, 
            required=True, 
            style={'input_type':'password'}
        )

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2', 'role')
        extra_kwargs = {
            'name':{'required': True},
            'role':{'required': True},
            'password':  {'write_only':True}
        }

    def validate(self, attrs): 
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password and Confirm Password didn't match."})
        
        if len(attrs['password']) < 8 or not any(char.isalpha() for char in attrs['password']):
            raise serializers.ValidationError("Password must be at least 8 characters long and contain at least one letter.")
        
        return attrs


    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        role      = validated_data.pop('role').lower()

        print("---------------------")
        print("role = ", role)
        print("---------------------")

        user = None
        if role == 'member':
            user = User.objects.create(
                name  = validated_data['name'],
                email = validated_data['email'],
                role  = 'member'
            )
        elif role == 'mentor':
            user = User.objects.create(
                name  = validated_data['name'],
                email = validated_data['email'],
                role  = 'mentor'
            )
        else:
            raise serializers.ValidationError({"Please select a role either `member` or `mentor`."})
        
        user.set_password(validated_data['password'])
        user.save()

        ## OTP Create of Varifications
        otp_obj = UserOTP.objects.create(user=user)

        # Email Send on Email
        html_content = render_to_string('mail/otp_mail.html', {
            'user': user,
            'code': otp_obj.otp
        })

        html_mail_sender(
            'Please verify your Account',  ## subject
            html_content,                  ## html_content
            [user.email],                  ## to
        )
           
        print("--------------------------------")
        print(f"Name= {user.name}, OTP= {otp_obj.otp}, Token= {otp_obj.token}")
        print("--------------------------------")

        return user


class UserRegistrationVerifySerializer(serializers.Serializer):
    user_otp = serializers.IntegerField()
    token    = serializers.CharField(max_length=100, required=True)

    class Meta:
        fields = ['user_otp', 'token']

        extra_kwargs = {
            'user_otp':{'required': True},
            'token'   :{'required': True},
        }

    def validate(self, attrs):
        user_otp = attrs.get('user_otp')
        token    = attrs.get('token')

        otp_user = UserOTP.objects.filter(token = token).first()
        if otp_user is not None:
            if otp_user.otp == user_otp:
                otp_time = otp_user.created_at

                # Make the timeout timezone-aware with the same timezone as otp_time
                timeout = otp_time + timedelta( minutes = settings.OTP_TIMEOUT )
                timeout = timeout.replace(tzinfo=otp_time.tzinfo)
                if datetime.now(timezone.utc) > timeout:
                    raise serializers.ValidationError("OTP verification time has expired")

                else:
                    otp_user.user.is_active = True
                    otp_user.user.is_verified = True
                    otp_user.user.save()
                    
                    otp_user.delete() # After the verification Delete the OTP
                    return attrs

            else:
                raise serializers.ValidationError("Your OTP doesn't match")

        else:
            raise serializers.ValidationError("Token is not exist!")


