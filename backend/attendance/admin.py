from django.contrib import admin
from .models import *
# Register your models here.


class UserImageAdmin(admin.ModelAdmin):
    list_display=['id','face_match','timestamp','Attendance','By_hr']



admin.site.register(Attendance,UserImageAdmin)