from django.db import models

class task(models.Model):
    task_name = models.CharField(max_length = 20, verbose_name = "任务名")
    publish_data = models.DateField(auto_now_add = True)
    deadline = models.DateField(verbose_name='结束时间')
    task_status = models.IntegerField(verbose_name='任务状态', choices=((0, '已挂起'), (-1, '已结束'), (1, '进行中')))
    members = models.CharField(max_length = 200, verbose_name='成员')
    all_members = models.CharField(max_length = 200, verbose_name='参加过项目的成员')
    task_description = models.CharField(max_length = 200, verbose_name='任务描述')
    task_need = models.CharField(max_length = 1000, verbose_name = '任务需求')
    task_schedule = models.CharField(max_length = 1000, verbose_name = '时间安排')
    appendixes = models.CharField(max_length = 200, verbose_name = '附件')
    task_progress = models.TextField(verbose_name = '任务进度')
    creator = models.IntegerField(verbose_name = '创建者')
    leader = models.CharField(max_length = 20, verbose_name = '组长')

    class Meta:
        permissions = {
            ('create_tasks','新建任务'),
            ('edit_tasks','编辑任务'),  # 面向实例
            ('glance_over_task_details', '浏览任务详情')  # 面向实例
        }