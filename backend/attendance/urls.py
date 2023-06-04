from django.urls import include, path
from .views import *


urlpatterns = [
    path('deepface/',attendacneView.as_view(),name='attendence using deep face')
]
