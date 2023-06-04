from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
User = get_user_model()


class locationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=location
        fields ="__all__"


class RegistrationSerializer(serializers.ModelSerializer):


    class Meta:
        model = User_Profile
     
        exclude = ('is_staff', 'is_active', 'Created_At', 'Updated_At','groups','user_permissions','isdeleted','is_superuser','FromDate','is_verified')

        
    def create(self, validated_data):
        user = User_Profile.objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.ModelSerializer):
    emp_id = serializers.CharField()
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


class UserImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    class Meta:
        model = UserImage
        fields = "__all__"
    
    
    
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     images = self.context['request'].FILES.getlist('image')
    #     for image in images:
    #         UserImage.objects.create(user=user, image=image)
    #         print(image)
    #     return validated_data