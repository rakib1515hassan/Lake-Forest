from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password       = serializers.CharField(write_only=True)

    def validate(self, atts):
        email_or_phone = atts.get("email_or_phone")
        password = atts.get("password")

        user = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()

        if user:
            if user.check_password(password) == False:
                raise serializers.ValidationError("Password is incorrect!")
            elif not user.is_active:
                raise serializers.ValidationError("The user is disabled!")
            else:
                usr = authenticate( email = user.email, password = password)
                atts["user"] = usr
                return atts
        
        raise serializers.ValidationError("Invalid login credentials!")

        