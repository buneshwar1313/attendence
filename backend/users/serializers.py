from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    User_Profile_image = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_null=True)


    class Meta:
        model = User_Profile
     
        exclude = ('is_staff', 'is_active', 'Created_At', 'Updated_At','groups','user_permissions','anonymous_id','isdeleted','is_superuser','FromDate','is_verified')

        
    def create(self, validated_data):
        user = User_Profile.objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.ModelSerializer):
    MobileNo = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User_Profile
        fields=[
            'emp_id',
            'password',
        ]



class ChangePasswordSerializer(serializers.Serializer):
    model = User_Profile
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)




class CurrentUserSerializer(serializers.ModelSerializer):
   
    # initialize fields

    class Meta:
        model = User_Profile
    
        exclude = ('is_staff', 'is_active', 'Created_At', 'Updated_At','groups','user_permissions','is_superuser','is_verified')
