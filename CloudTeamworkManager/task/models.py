from django.db import models

class task(models.Model):
    publish_data = models.DateField()
    deadline = models.DateField()
    task_status = models.CharField(max_length = 1)
    members_info = models.CharField(max_length = 200)
    task_description = models.CharField(max_length = 200)
    task_need = models.CharField(max_length = 1000)
    task_schedule = models.CharField(max_length = 1000)
    appendixes = models.CharField(max_length = 200)
    task_progress = models.TextField()

    class Meta:
        permissions = {
            ('create_tasks','新建任务的权限'),
        }