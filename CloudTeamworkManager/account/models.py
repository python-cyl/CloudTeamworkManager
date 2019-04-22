from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 5, verbose_name='姓名')
    student_id = models.CharField(max_length = 11, verbose_name='学号')
    cloud_id = models.CharField(max_length = 20, verbose_name='云顶号')
    phone_number = models.CharField(max_length = 11, verbose_name='手机号')
    email = models.CharField(max_length = 30, verbose_name='邮箱')
    magor = models.CharField(max_length = 10, verbose_name='方向')
    grade = models.CharField(max_length = 4, verbose_name='年级')
    room = models.CharField(max_length = 8, verbose_name='宿舍号')
    home_address = models.CharField(max_length = 300, verbose_name='家庭住址')
    guardian_phone = models.CharField(max_length = 11, verbose_name='家长手机号')
    introduction = models.CharField(max_length = 350, verbose_name='个人介绍')
    involved_projects = models.TextField()
    read_notifications = models.TextField()
    unread_notifications = models.TextField()
    sex = models.NullBooleanField(verbose_name='性别')
