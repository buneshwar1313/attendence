from .models import *
from django.shortcuts import render
from rest_framework import generics , permissions , mixins , status
from django.contrib.auth import login as django_login,authenticate,logout as django_logout
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework import serializers
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework.response import Response
from django.core import serializers
import json
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_200_OK
from random import randint
from django.conf import settings
from twilio.rest import Client
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.response import Response



"""Registration Serializer"""

class registration(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = RegistrationSerializer
    queryset = User_Profile.objects.all()
    lookup_field = 'id'


    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            print(request)           
            return self.list(request)

    # def delete(self, request, id=None):
    #     return self.destroy(request, id)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"data":serializer.data["id"],"message":"User Register successfully"})
        else:
            return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)





"""Login Serializer"""

class loginView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = LoginSerializer
    queryset = User_Profile.objects.all()

    def post(self, request):
        username = request.data.get("emp_id")
        password = request.data.get("password")
      
        if username is None or password is None:
            return Response({'error': 'Please provide both MobileNo and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
                    return Response({'error': 'Invalid Credentials'},
                                    status=HTTP_404_NOT_FOUND)
        

        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key,'User_Id':user.id,'message':'Login Successfully','hr_verify':user.hr_verify,'emp_id_verify':user.emp_id_verify},
                            status=HTTP_200_OK)




"""Logout Serializer"""
   
# Logout Employee
class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request, format=None):
        # simply delete the token to force a login
        self.request.user.auth_token.delete()
        return Response({'message': 'Logout Success'}, status=HTTP_200_OK)

class LogoutView(APIView):

    authentication_classes=(TokenAuthentication,)
    queryset = User_Profile.objects.all()

    def get(self, request, format=None):
        django_logout(request)
        return Response({'message':'logout done'},status=200)





"""Change Password"""



class ChangePasswordView(GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User_Profile
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response({"error": serializer.errors},status=HTTP_400_BAD_REQUEST)
       


""" Forgot Pasword"""



"""Get current User Details"""
class getCurrentUserView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = CurrentUserSerializer
    queryset = User_Profile.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return User_Profile.objects.filter(id=self.request.user.id)


    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)



"""Get User Details"""
class getallusersView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = CurrentUserSerializer
    queryset = User_Profile.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def get_queryset(self):
        return User_Profile.objects.all()
    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)




"""Get User Details"""

class UploadImages(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserImageSerializer
    queryset = UserImage.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # def get_queryset(self):
    #     return UserImage.objects.filter(user=self.request.id)

    def get(self, request, id=None):
        data = UserImage.objects.filter(user=self.request.user)
        serialized_data = UserImageSerializer(data, many=True).data
        return Response(serialized_data, status=200)

    def post(self, request):
            
        user = request.user
        images = request.FILES.getlist('image')
        print(user)
        print(images)
        for i, image in enumerate(images):
            if i >= 5:
                break

            # Generate a unique filename for each image
            emp_id = user.emp_id  # Assuming emp_id is the field in User_Profile model
            filename = f"emp_{emp_id}_image_{i + 1}.jpg"  # Replace with your desired naming convention

            # Create the UserImage instance with the user and renamed image
            user_image = UserImage(user=user, image=image)
            user_image.image.name = filename  # Assign the new filename to the image field
            user_image.save()
            print("user_image",user_image)

        return Response("hello", status=status.HTTP_201_CREATED)
    




