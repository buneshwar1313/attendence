from django.contrib import admin
from .models import *
# Register your models here.

class UserImageAdmin(admin.ModelAdmin):
    list_display=['id','image']


admin.site.register(User_Profile)
admin.site.register(UserImage,UserImageAdmin)