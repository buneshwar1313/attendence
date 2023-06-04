from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
User = get_user_model()



class attendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields='__all__'
