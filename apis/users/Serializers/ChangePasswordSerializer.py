from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
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
        fields = ['old_password', 'password', 'password2']

    def validate_password(self, value):
        password = self.initial_data.get('password')
        password2 = self.initial_data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        if len(password) < 8 or not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Password must be at least 8 characters long and contain at least one letter.")

        return value



    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password  = attrs.get('password')
        password2 = attrs.get('password2')
        
        user     = self.context.get('user') 
        get_user = User.objects.filter( email = user.email ).first()

        if get_user:
            if not authenticate( email = get_user.email, password = old_password):
                raise serializers.ValidationError("Old password is incorrect")
            else:
                get_user.set_password(password)
                get_user.save()
                return attrs
            
        raise serializers.ValidationError("Validation error!")
