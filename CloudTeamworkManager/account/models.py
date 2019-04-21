from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 5)
    student_id = models.CharField(max_length = 11)
    cloud_id = models.CharField(max_length = 20)
    phone_number = models.CharField(max_length = 11)
    email = models.CharField(max_length = 30)
    magor = models.CharField(max_length = 10)
    grade = models.CharField(max_length = 4)
    room = models.CharField(max_length = 8)
    home_address = models.CharField(max_length = 300)
    guardian_phone = models.CharField(max_length = 11)
    introduction = models.CharField(max_length = 350)
    involved_projects = models.TextField()
    read_notifications = models.TextField()
    unread_notifications = models.TextField()
    sex = models.NullBooleanField()
