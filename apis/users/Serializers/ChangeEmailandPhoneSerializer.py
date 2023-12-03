from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()
from apis.users.utils import OTP_Send
from django.template.loader import render_to_string
from apps.core.utils import html_mail_sender, sms_sender
from apps.users.models import UserOTP

from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

class UserEmailChangeSerializer(serializers.Serializer):
    password = serializers.CharField( write_only=True, required=True, style={'input_type':'password'})
    new_email = serializers.EmailField(max_length=255, style={'input_type': 'email'}, write_only=True)

    class Meta:
        fields = ['new_email', 'password']

    def validate(self, attrs):
        password  = attrs.get('password')
        new_email = attrs.get('new_email')
        user    = self.context.get('user')
        otp_obj = self.context.get('otp_obj')

        if user:
            if not authenticate( email = user.email, password = password):
                raise serializers.ValidationError("You password is incorrect!")
            else:
                if not new_email == user.email:
                    self.context['request'].session['email'] = new_email ## New Email store in  Django session

                    # html_content = render_to_string('mail/otp_mail.html', {
                    #     'user': user,
                    #     'code': otp_obj.otp
                    # })

                    # html_mail_sender(
                    #     'AddressPMS account Email change',  ## subject
                    #     html_content,                       ## html_content
                    #     [new_email],                        ## to
                    # )
                    
                    ## Phone varification
                    # body = f"""
                    #             Welcome to Address PMS
                    #             Hi, {user.name}, .
                    #             Your verification OTP is {otp_obj.otp}

                    #             Regards,
                    #             Address PMS Team
                    #     """
                    # sms_sender (
                    #     user.phone,
                    #     body,
                    # )
                    return attrs   
                else:
                     raise serializers.ValidationError("This email already used!")
            
        raise serializers.ValidationError("Validation error!")




class UserPhoneChangeSerializer(serializers.Serializer):
    new_phone = serializers.CharField(max_length=255, style={'input_type': 'text'}, write_only=True)
    password  = serializers.CharField( write_only=True, required=True, style={'input_type':'password'})

    class Meta:
        fields = ['new_phone', 'password']

    def validate(self, attrs):
        password  = attrs.get('password')
        new_phone = attrs.get('new_phone')
        user    = self.context.get('user')
        otp_obj = self.context.get('otp_obj')

        if user:
            if not authenticate( email = user.email, password = password):
                raise serializers.ValidationError("You password is incorrect!")
            else:
                if not new_phone == user.phone:
                    self.context['request'].session['phone'] = new_phone ## New Phone store in  Django session

                    # html_content = render_to_string('mail/otp_mail.html', {
                    #     'user': user,
                    #     'code': otp_obj.otp
                    # })

                    # html_mail_sender(
                    #     'AddressPMS account Email change',  ## subject
                    #     html_content,                       ## html_content
                    #     [user.email],                        ## to
                    # )
                    
                    # Phone varification
                    # body = f"""
                    #             Welcome to Address PMS
                    #             Hi, {user.name}, .
                    #             Your verification OTP is {otp_obj.otp}

                    #             Regards,
                    #             Address PMS Team
                    #     """
                    # sms_sender (
                    #     new_phone,
                    #     body,
                    # )
                    return attrs
                else:
                     raise serializers.ValidationError("This phone already used!")
        raise serializers.ValidationError("Validation error!")







class Email_Change_OTPVerificationSerializer(serializers.Serializer):
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

        user    = self.context.get('user')
        new_email   = self.context['request'].session.get('email')  ## New Email get from  Django session

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
                    user.email = new_email
                    user.save()
                    return attrs
            
            raise serializers.ValidationError("OTP doesn't match.")
            
        raise serializers.ValidationError("Token is not valid!")




class Phone_Change_OTPVerificationSerializer(serializers.Serializer):
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

        user    = self.context.get('user')
        new_phone   = self.context['request'].session.get('phone')  ## New Phone number get from  Django session
        
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
                    user.phone = new_phone
                    user.save()
                    return attrs
            
            raise serializers.ValidationError("OTP doesn't match.")
            
        raise serializers.ValidationError("Token is not valid!")