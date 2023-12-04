from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.exceptions import ValidationError


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model   = User
        exclude = ['password', 'user_permissions', 'groups', 'updated_at', 'last_login']
        # fields  = '__all__'
        # fields = ('id','name', 'email', 'phone', 'dob', 'gender', 'division', 'sub_division', 'zip_code', 'home')

        extra_kwargs = {
            'is_verified'  : {'read_only': True},
            'is_active'    : {'read_only': True},
            'is_admin'     : {'read_only': True},
            'is_superuser' : {'read_only': True},
            'created_at'   : {'read_only': True},
            'role'         : {'read_only': True},
            'email'        : {'read_only': True},
            'name'         : {'required': True},
        }

    # id = serializers.UUIDField(source='pk', format='hex', read_only=True)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Convert the 'id' field to a string
    #     data['id'] = str(instance.id)
    #     return data






# class CustomerSerializer(serializers.ModelSerializer):
    # is_verified   = serializers.ReadOnlyField()
    # is_active     = serializers.ReadOnlyField()
    # is_admin      = serializers.ReadOnlyField()
    # is_superuser  = serializers.ReadOnlyField()
    # created_at    = serializers.ReadOnlyField()
    # user_type     = serializers.ReadOnlyField()
    # auth_provider = serializers.ReadOnlyField()
    # email         = serializers.ReadOnlyField()
    # phone         = serializers.ReadOnlyField()

    # class Meta:
    #     model   = User
    #     exclude = ['password', 'user_permissions', 'groups', 'updated_at', 'last_login']