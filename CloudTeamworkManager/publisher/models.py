from django.db import models


class personal_comment(models.Model):
    detail = models.TextField(verbose_name = '内容', default = "[]")
    id = models.CharField(max_length = 15, primary_key = True)

class personal_progress(models.Model):
    detail = models.TextField(verbose_name = '内容')
    id = models.CharField(max_length = 15, primary_key = True, default = "[]")

    class Meta:
        permissions = {
            #('view_personal_progress', '查看个人进度'), 
            ('edit_personal_progress', '编辑个人进度'), 
        }

class personal_shedule(models.Model):
    detail = models.TextField(verbose_name = '内容', default = "[]")
    id = models.CharField(max_length = 15, primary_key = True)

    class Meta:
        permissions = {
            #('view_personal_shedule', '查看个人时间表'), 
            ('edit_personal_shedule', '编辑个人时间表'), 
        }
