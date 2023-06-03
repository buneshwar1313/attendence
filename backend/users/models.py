from enum import unique
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.conf import settings
User = settings.AUTH_USER_MODEL
import uuid
from django.conf import settings
User = settings.AUTH_USER_MODEL
import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator, validate_email
from django_resized import ResizedImageField
from time import timezone
from datetime import datetime





# Create your models here.
class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, emp_id, password=None,*args,**kwargs):
        """create a new user profile"""

        if not emp_id:
            raise ValueError("User must have an Mobile Number")
        # emp_id = self.normalize_email(emp_id)
        user = self.model(emp_id=emp_id,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, emp_id, password):
        """create and save new super user with given dertails"""
        user = self.create_user(emp_id, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user




   

class User_Profile(AbstractBaseUser,PermissionsMixin):
  
    user_Full_Name = models.CharField(max_length=100,null=True,blank=True)
    email_Id=models.EmailField(max_length=200,unique=True,null=True)
    user_Profile_Image = ResizedImageField(scale=0.5,force_format='PNG', quality=75,upload_to='user_profile_image/',blank=True,null=True)
    emp_id = models.CharField(max_length=10,null=True, blank=True,unique=True)
    FromDate=models.DateTimeField(blank=True,null=True)
    emp_id_verify = models.BooleanField(default=False)
    hr_verify=models.BooleanField(default=False)
    isdeleted=models.BooleanField(default=False,null=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    Created_At=models.DateTimeField(auto_now_add=True, null=True)
    Updated_At=models.DateTimeField(auto_now_add=True,null=True)


    objects = UserManager()
    USERNAME_FIELD = 'emp_id'



    class Meta:
        ordering=["-Created_At"]
    def __str__(self):
        return f"{self.id}, {self.Uuer_Full_Name}, {self.emp_id}, "
    

class UserImage(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='user_images/')

    def __str__(self):
        return f"Image {self.id} for User {self.user.emp_id}"

