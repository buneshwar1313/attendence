from django.db import models
from users.models import User_Profile
# Create your models here.


class Attendance(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    face_match = models.BooleanField(default=False)
    Attendance=models.BooleanField(default=False)
    By_hr =models.BooleanField(default=False)



    def __str__(self):
        return f'{self.user.emp_id} -{self.timestamp}'
