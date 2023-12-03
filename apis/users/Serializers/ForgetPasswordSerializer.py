from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.template.loader import render_to_string
from apps.core.utils import html_mail_sender, sms_sender
from apps.users.models import UserOTP
from datetime import datetime, timedelta
from django.utils import timezone

# Sending Mail
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()
import random




class FP_OTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()

        if user:    
            if UserOTP.objects.filter(user = user).exists():
                UserOTP.objects.get(user = user).delete()

            otp_obj = UserOTP.objects.create(user = user)

            html_content = render_to_string('mail/forget_password_mail.html', {
                'user': user,
                'code': otp_obj.otp
            })

            html_mail_sender(
                'Recover your account.',  ## subject
                html_content,                  ## html_content
                [user.email],                  ## to
            )
            
            ## Phone varification
            body = f"""
                        Welcome to Address PMS
                        Hi, {user.name}, 
                        To recover your account.
                        Your verification OTP is {otp_obj.otp}

                        Regards,
                        Address PMS Team
                """
            sms_sender (
                user.phone,
                body,
            )

            # print("--------------------------------")
            # print(f"User Name : {user.name}, User Otp : {otp_obj.otp}")
            # print("--------------------------------")

            return attrs
        
        raise serializers.ValidationError('Unregistered User!')




class FP_OTPVerificationSerializer(serializers.Serializer):
    user_otp = serializers.IntegerField(required=True)
    token    = serializers.CharField(max_length=100, required=True)

    class Meta:
        fields = ['user_otp', 'token']

        extra_kwargs = {
            'user_otp':{'required': True},
            'token'   :{'required': True},
        }

    def validate(self, attrs):
        otp_token = attrs.get('token') 
        user_otp  = attrs.get('user_otp')

        otp_user = UserOTP.objects.filter(token = otp_token).first()
        if otp_user is not None:
            if otp_user.otp == user_otp:
                otp_time = otp_user.created_at

                # Make the timeout timezone-aware with the same timezone as otp_time
                timeout = otp_time + timedelta( minutes = settings.OTP_TIMEOUT )
                timeout = timeout.replace(tzinfo=otp_time.tzinfo)

                current_time = timezone.now()

                if current_time > timeout:
                    raise serializers.ValidationError("OTP verification time has expired.")

                else:
                    otp_user.is_used = True
                    otp_user.save()
                    return attrs
            
            raise serializers.ValidationError("OTP doesn't match.")
            
        raise serializers.ValidationError("Token is not valid!")





class FP_PasswordSetSerializer(serializers.Serializer):
    password  = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    token     = serializers.CharField(max_length=100, required=True)
    class Meta:
        fields = ['password', 'password2', 'token']


    # Password must be at least 8 characters long and contain at least one letter.
    def validate_password(self, value):
        password  = self.initial_data.get('password')
        password2 = self.initial_data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        if len(password) < 8 or not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Password must be at least 8 characters long and contain at least one letter.")

        return value
    
    
    def validate(self, attrs):
        otp_token = attrs.get('token')
        password  = attrs.get('password')
        password2 = attrs.get('password2')
     
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        
        otp_obj = UserOTP.objects.filter(token = otp_token).first()

        if otp_obj:
            if otp_obj.is_used:
                otp_obj.user.set_password(password)
                otp_obj.user.save()
                otp_obj.delete()
                return attrs

            else:
                raise serializers.ValidationError("Please match OTP first, then set password!")

        raise serializers.ValidationError("Unregistered User!")




class FP_OTPResendSerializer(serializers.Serializer):
    token    = serializers.CharField(max_length=100, required=True)

    class Meta:
        fields = ['token']

        extra_kwargs = {
            'token'   :{'required': True},
        }
    
    def validate(self, attrs):
        otp_token = attrs.get('token')

        otp_obj = UserOTP.objects.filter(token = otp_token).first()
        user    = User.objects.filter(id = otp_obj.user.id).first()

        if otp_obj and user:    
            otp_obj.delete()

            new_otp_obj = UserOTP.objects.create(user = user)

            html_content = render_to_string('mail/forget_password_mail.html', {
                'user': user,
                'code': new_otp_obj.otp
            })

            html_mail_sender(
                'Recover your account.',  ## subject
                html_content,             ## html_content
                [user.email],             ## to
            )
            
            ## Phone varification
            body = f"""
                        Welcome to Address PMS
                        Hi, {user.name}, 
                        To recover your account.
                        Your verification OTP is {new_otp_obj.otp}

                        Regards,
                        Address PMS Team
                """
            sms_sender (
                user.phone,
                body,
            )

            # print("--------------------------------")
            # print(f"User Name : {user.name}, User Otp : {new_otp_obj.otp}")
            # print("--------------------------------")

            return attrs
        
        raise serializers.ValidationError('Unregistered User!')