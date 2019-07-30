from django.db import models


class task(models.Model):
    task_name = models.CharField(max_length = 20, verbose_name = "任务名")
    publish_date = models.DateField(auto_now_add = True)
    deadline = models.DateField(verbose_name='结束时间')
    task_status = models.IntegerField(verbose_name='任务状态', choices=((0, '已挂起'), (-1, '已结束'), (1, '进行中')))
    members = models.CharField(max_length = 200, verbose_name='成员', default = "[]")
    all_members = models.CharField(max_length = 200, verbose_name='参加过项目的成员', default = "[]")
    creator = models.IntegerField(verbose_name = '创建者')
    leaders = models.CharField(max_length = 20, verbose_name = '组长', default = "[]")
    task_description = models.CharField(max_length = 200, verbose_name='任务描述', default = "")
    task_need = models.CharField(max_length = 1000, verbose_name = '任务需求', default = "")
    task_schedule = models.TextField(verbose_name = '时间安排', default = '[]')
    task_progress = models.TextField(verbose_name = '任务进度', default = "[]")
    task_comment = models.TextField(verbose_name = '任务评价', default = "[]")
    appendixes = models.CharField(max_length = 200, verbose_name = '附件', default = "[]")

    # 这里对权限进行定义
    class Meta:
        permissions = {
            ('create_tasks','新建任务'),
            ('edit_tasks','编辑任务'),  # 面向实例
            ('glance_over_task_details', '浏览任务详情'),  # 面向实例
            ('view_personal_comments','查看个人评价'),  # 面向实例
            ('edit_personal_comments','编辑个人评价'),  # 面向实例
            ('edit_progress', '编辑任务时间表'),  # 面向实例
            ('edit_shedule', '编辑任务进度'),  # 面向实例
            ('view_personal_progress', '查看个人进度'),  # 面向实例
            ('view_personal_shedule', '查看个人时间表'),  # 面向实例
            ('edit_appendix', '编辑附件'),  # 面向实例
            ('delete_appendix', '删除附件'),  # 面向实例
        }
