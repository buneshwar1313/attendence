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
        username = request.data.get("MobileNo")
        password = request.data.get("password")
      
        if username is None or password is None:
            return Response({'error': 'Please provide both MobileNo and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
                    return Response({'error': 'Invalid Credentials'},
                                    status=HTTP_404_NOT_FOUND)
        

        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key,'User_Id':user.id,'Wallet_Id':wall.id,'message':'Login Successfully'},
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










