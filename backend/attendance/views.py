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

from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.response import Response

from .deepface.match import face_match

from django.core.files.uploadedfile import InMemoryUploadedFile





class attendacneView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = attendanceSerializer
    queryset = Attendance.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

 

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)
        
    def perform_create(self, serializer):
       
        serializer.save(User=self.request.user)


    def delete(self, request, id=None):
        return self.destroy(request, id)

    def post(self, request):
        data = request.data
        unknown_image = request.FILES.get("image")
        print(unknown_image)
        user=self.request.user
        facematch=face_match(unknown_image,user)
        print("replay from deep face ",facematch)
        if  facematch:
            mark_attendence= Attendance.objects.create(user=request.user,face_match=facematch,Attendance=True)
            return Response({"message":"Attendance Marked"})
        mark_attendence= Attendance.objects.create(user=request.user,face_match=facematch)
        return Response({"message":"Face not recognise"})


    def put(self, request, id=None):
        return self.update(request, id)

    def patch(self,request, id =None):
        return self.partial_update(request,id)

