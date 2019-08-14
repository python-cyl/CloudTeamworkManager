from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User, Group, Permission
from guardian.shortcuts import assign_perm, remove_perm
from task.models import task as models_task
from task.forms import task as forms_task
from publisher.models import personal_comment, personal_progress, personal_shedule
from account.models import UserProfile
import re
import json
import time


class user(object):
    user_buildin = None
    user_profile = None

    def __init__(self, user_id, **kw):
        self.user_buildin = User.objects.get(id = user_id)
        self.user_profile = UserProfile.objects.get(user_id = user_id)

    def join_task(self, create_archive = True, **kw):
        def create_personal_archive():
            personal_comment.objects.create(id = "%s&%s"%(target_task.id, self.user_buildin.id), detail = "[]")
            temp = personal_progress.objects.create(id = "%s&%s"%(target_task.id, self.user_buildin.id), detail = "[]")
            assign_perm('publisher.edit_personal_progress', self.user_buildin, temp)
            assign_perm('publisher.view_personal_progress', self.user_buildin, temp)
            temp = personal_shedule.objects.create(id = "%s&%s"%(target_task.id, self.user_buildin.id), detail = "[]")
            assign_perm('publisher.edit_personal_shedule', self.user_buildin, temp)
            assign_perm('publisher.view_personal_shedule', self.user_buildin, temp)

        def recover_archive_edit_perm():
            assign_perm('publisher.edit_personal_progress', self.user_buildin, personal_progress.objects.get(id = "%s&%s"%(target_task.id, self.user_buildin.id)))
            assign_perm('publisher.edit_personal_shedule', self.user_buildin, personal_shedule.objects.get(id = "%s&%s"%(target_task.id, self.user_buildin.id)))

        if "task_id" in kw:
            target_task = models_task.objects.get(id = kw["task_id"])
        elif "target_task" in kw:
            target_task = kw["target_task"]
        else:
            pass
            # 这里需要抛出异常，缺少定位task的条件

        if "target_group" in kw:
            target_group = kw["target_group"]
        else:
            targer_group = Group.objects.get(name = str(target_task.id))
        
        self.user_profile.involved_projects_number += 1
        temp = json.loads(self.user_profile.involved_projects)
        temp.append(target_task.id)
        self.user_profile.involved_projects = json.dumps(temp)
        self.user_profile.save()

        temp = json.loads(target_task.members)
        temp.append(self.user_buildin.id)
        temp = list(set(temp))
        target_task.members = json.dumps(temp)

        temp.extend(json.loads(target_task.all_members))
        target_task.all_members = json.dumps(list(set(temp)))
        
        target_task.save()
            
        self.user_buildin.groups.add(target_group)

        if create_archive:
            create_personal_archive()
        else:
            recover_archive_edit_perm()

class member(user):
    task = None
    is_leader = False

    def __init__(self, user_id, **kw):
        super(member, self).__init__(user_id, **kw)

        if "target_task" in kw:
            self.task = kw["target_task"]
        elif "task_id" in kw:
            self.task = models_task.objects.get(id = kw["target_id"])
        else:
            pass
            # 这里需要抛出异常，缺少定位task的条件

        if not self.user_buildin.id in json.loads(self.task.members):
            pass
            # 这里需要抛出异常，用户不是该项目组的成员

        if self.user_buildin.id in json.loads(self.task.leaders):
            self.is_leader = True

    def quit_task(self, **kw):
        # 如果这个人是组长，先取消组长职位。
        # 不建议批量使用此方法移除组长，因为获取组长用户组会增加数据库负担
        if self.is_leader:
            self.cancel_leader(Group.objects.get(name = "%s%s"%(str(self.task.id), "leaders")))

        if "target_group" in kw:
            target_group = kw["target_group"]
        else:
            target_group =  Group.objects.get(name = str(self.task.id))

        self.task.members = json.dumps(json.loads(self.task.members).remove(self.user_buildin.id))
        self.task.save()

        self.user_profile.involved_projects = json.dumps(json.loads(self.user_profile.involved_projects).remove(self.task.id))
        self.user_profile.involved_projects_num -= 1;
        self.user_profile.save()

        self.user_buildin.groups.remove(target_group)
        remove_perm('publisher.edit_personal_progress', self.user, personal_progress.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id)))
        remove_perm('publisher.edit_personal_shedule', self.user, personal_shedule.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id)))

    def view_personal_comments(self, request):
        if request.user.has_perm("task.view_personal_comments", self.task):
            comment = personal_comment.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id))

            return HttpResponse(comment.detail)
        return HttpResponse(status=403)
    
    def edit_personal_comments(self, request):
        if request.user.has_perm("task.edit_personal_comments", self.task):
            comment = personal_comment.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id))
            
            if request.POST.get("action") == "upgrade":
                comment.detail = _publisher(comment.detail).upgrade(request.POST.get("content"))
            elif request.POST.get("action") == "create":
                comment.detail = _publisher(comment.detail).create(request.POST.get("content"), editor_id = request.user.id)
            comment.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status=403)

    def view_personal_shedule(self, request):
        shedule = personal_shedule.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.view_personal_shedule", shedule) or request.user.has_perm("task.view_personal_shedule", self.task):
            return HttpResponse(shedule.detail)
        return HttpResponse(status=403)

    def edit_personal_shedule(self, request):
        shedule = personal_shedule.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.edit_personal_shedule", shedule):
            if request.POST.get("action") == "upgrade":
                shedule.detail = _publisher(shedule.detail).upgrade(request.POST.get("content"))
            elif request.POST.get("action") == "create":
                shedule.detail = _publisher(shedule.detail).create(request.POST.get("content"))
            shedule.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status=403)

    def view_personal_progress(self, request):
        progress = personal_progress.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.view_personal_progress", progress) or request.user.has_perm("task.view_personal_progress", self.task):
            return HttpResponse(progress.detail)
        return HttpResponse(status=403)

    def edit_personal_progress(self, request):
        progress = personal_progress.objects.get(id = "%s&%s"%(self.task.id, self.user_buildin.id))

        if request.user.has_perm("publisher.edit_personal_progress", progress):
            if request.POST.get("action") == "upgrade":
                progress.detail = _publisher(progress.detail).upgrade(request.POST.get("content"))
            elif request.POST.get("action") == "create":
                progress.detail = _publisher(progress.detail).create(request.POST.get("content"))
            progress.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status=403)

    def cancel_leader(self, target_group):
        if self.is_leader:
            self.task.leaders = json.dumps(json.loads(self.task.leaders).remove(self.user_buildin.id))
            self.task.save()

            temp = json.loads(self.user_buildin.managed_projects)
            temp.remove(self.task.id)
            self.user_buildin.managed_projects = json.dumps(temp)
            self.user_buildin.managed_projects_number -= 1
            self.user_buildin.save()

            self.user_buildin.groups.remove(target_group)
        else:
            pass
            # 这里需要抛出异常，用户不是该项目组的组长

    def set_leader(self, target_group):
        if not self.is_leader:
            temp = json.loads(self.task.leaders)
            if not self.user_buildin.id in temp:
                temp.append(self.user_buildin.id)

            self.task.leaders = json.dumps(temp)
            self.task.save()

            temp = json.loads(self.user_profile.managed_projects)
            temp.append(self.task.id)
            self.user_profile.managed_projects = json.dumps(temp)
            self.user_profile.managed_projects_number += 1
            self.user_profile.save()

            self.user_buildin.groups.add(target_group)
        else:
            pass
            # 这里需要抛出异常，用户已是该项目组的组长

class creater(member):
    def __init__(self, user_id, **kw):
        super(creater, self).__init__(user_id, **kw)

        if not self.user_buildin.id == self.task.creater:
            pass
            # 这里需要抛出异常，用户不是该项目组的创建者

    def remove_permissions(self):
        remove_perm('task.edit_task', request.user, target_task)
        remove_perm('task.edit_task_comments', request.user, target_task)
        remove_perm('task.view_personal_comments', request.user, target_task)
        remove_perm('task.view_personal_progress', request.user, target_task)
        remove_perm('task.view_personal_shedule', request.user, target_task)
        remove_perm('task.edit_appendix', request.user, target_task)
        remove_perm('task.delete_appendix', request.user, target_task)

class task(object):
    task = None

    def __init__(self, task_id):
        self.task = models_task.objects.get(id = task_id)

    def view_task_comment(self, request):
        if request.user.has_perm("task.glance_over_task_details", self.task):
            return HttpResponse(self.task.task_comment)
        return HttpResponse(status = 403)

    def edit_task_comment(self, request):
        if request.user.has_perm("task.edit_task_comments", self.task):
            if request.POST.get("action") == "upgrade":
                self.task.task_comment = _publisher(self.task.task_comment).upgrade(request.POST.get("content"), editor_id = request.user.id)
            elif request.POST.get("action") == "create":
                self.task.task_comment = _publisher(self.task.task_comment).create(request.POST.get("content"), editor_id = request.user.id)
            self.task.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status = 403)

    def view_task_progress(self, request):
        if request.user.has_perm("task.glance_over_task_details", self.task):
            return HttpResponse(self.task.task_progress)
        return HttpResponse(status = 403)

    def edit_task_progress(self, request):
        if request.user.has_perm("task.edit_task_progress", self.task):
            if request.POST.get("action") == "upgrade":
                self.task.task_progress = _publisher(self.task.task_progress).upgrade(request.POST.get("content"), editor_id = request.user.id)
            elif request.POST.get("action") == "create":
                self.task.task_progress = _publisher(self.task.task_progress).create(request.POST.get("content"), editor_id = request.user.id)
            self.task.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status = 403)

    def view_task_shedule(self, request):
        if request.user.has_perm("task.glance_over_task_details", self.task):
            return HttpResponse(self.task.task_schedule)
        return HttpResponse(status = 403)

    def edit_task_shedule(self, request):
        if request.user.has_perm("task.edit_task_shedule", self.task):
            if request.POST.get("action") == "upgrade":
                self.task.task_schedule = _publisher(self.task.task_schedule).upgrade(request.POST.get("content"), editor_id = request.user.id)
            elif request.POST.get("action") == "create":
                self.task.task_schedule = _publisher(self.task.task_schedule).create(request.POST.get("content"), editor_id = request.user.id)
            self.task.save()
                
            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return HttpResponse(status = 403)

    @staticmethod
    def create_page(request):
        return render(request, "create_task.html")

    @staticmethod
    def create_task(request):
        form = forms_task(request.POST)

        if form.is_valid():
            form.instance.all_members = form.instance.members
            form.instance.creator = request.user.id

            target_task = form.save()

            # 用户组
            target_group = Group.objects.create(name=str(target_task.id))

            # 为一个组对一个对象分配权限
            assign_perm('task.glance_over_task_details', target_group, target_task)

            # 组长组
            target_group_leaders = Group.objects.create(name = "%s%s"%(str(target_task.id), "leaders"))

            # 为组长组分配权限
            assign_perm('task.view_personal_comments', target_group_leaders, target_task)
            assign_perm('task.edit_personal_comments', target_group_leaders, target_task)
            assign_perm('task.edit_task_progress', target_group_leaders, target_task)
            assign_perm('task.edit_task_shedule', target_group_leaders, target_task)
            assign_perm('task.view_personal_progress', target_group_leaders, target_task)
            assign_perm('task.view_personal_shedule', target_group_leaders, target_task)
            assign_perm('task.edit_appendix', target_group_leaders, target_task)
            assign_perm('task.delete_appendix', target_group_leaders, target_task)

            # 配置创建者权限
            request.user.groups.add(target_group)
            assign_perm('task.edit_task', request.user, target_task)
            assign_perm('task.edit_task_comments', request.user, target_task)
            assign_perm('task.view_personal_comments', request.user, target_task)
            assign_perm('task.view_personal_progress', request.user, target_task)
            assign_perm('task.view_personal_shedule', request.user, target_task)
            assign_perm('task.edit_appendix', request.user, target_task)
            assign_perm('task.delete_appendix', request.user, target_task)
            
            # 配置组员相关
            for each in json.loads(form.instance.members):
                try:
                    target_user = user(user_id = each)
                except UserProfile.DoesNotExist:
                    continue

                target_user.join_task(target_task = target_task, target_group = target_group)

            # 配置组长相关
            for each in json.loads(form.instance.leaders):
                try:
                    target_member = member(user_id = each, target_task = target_task)
                except UserProfile.DoesNotExist:
                    continue

                target_member.set_leader(target_group = target_group_leaders)

            # 通知

            return JsonResponse({"url": "/task/%d"%target_task.id, "status": 302}, safe=False)
        return JsonResponse({"tip": "表单验证失败", "status": 400}, safe=False)

    # 需要修改
    def edit_page(self, request):
        return render(request, "create_task.html")

    def edit_task(self, request):
        form = forms_task(request.POST, instance = self.task)

        if form.is_valid():
            # 重新获取task实例，因为is_valid修改了task实例。似乎是个bug？
            self.task = models_task.objects.get(id = self.task.id)
            # 计算新增成员和被移除的成员
            past_members = set(json.loads(self.task.members))
            current_members = set(json.loads(form.instance.members))
            removed_members = past_members - current_members
            new_members = current_members - past_members

            # 计算新增组长和被移除的组长
            past_leaders = set(json.loads(self.task.leaders))
            current_leaders = set(json.loads(form.instance.leaders))
            removed_leaders = past_leaders - current_leaders
            new_leaders = current_leaders - past_leaders

            # 获取权限组
            target_group = Group.objects.get(name=str(self.task.id))
            target_group_leader = Group.objects.get(name = "%s%s"%(str(self.task.id), "leaders"))

            # 更新参与过该任务的成员列表
            form.instance.all_members = json.dumps(list(set(json.loads(form.instance.all_members) + list(current_members))))
            form.save()

            # 撤销组长
            for each in removed_leaders:
                try:
                    target_member = member(user_id = each, target_task = self.task)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                target_member.cancel_leader(target_group_leader)

                # 通知

            # 移除组员
            for each in removed_members:
                try:
                    target_member = member(user_id = each, target_task = self.task)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                target_member.quit_task(target_group = target_group)

                # 通知

            # 配置新增组员
            for each in new_members:
                try:
                    target_user = user(user_id = each)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                if each in json.loads(self.task.all_members):
                    target_user.join_task(create_archive = False, target_task = self.task, target_group = target_group)
                else:
                    target_user.join_task(create_archive = True, target_task = self.task, target_group = target_group)

                # 通知

            # 配置新增组长
            for each in new_leaders:
                try:
                    target_member = member(user_id = each, target_task = self.task)
                except UserProfile.DoesNotExist:
                    continue
                except User.DoesNotExist:
                    continue

                target_member.set_leader(target_group_leader)

                # 通知

            return JsonResponse({"url": "/task/%d"%self.task.id, "status": 302}, safe=False)
        return JsonResponse({"tip": "表单验证失败", "status": 400}, safe=False)

    def delete_task(self, request):
        members = json.loads(self.task.members)
        leaders = json.loads(self.task.leaders)

        # 撤销权限
        target_group = Group.objects.get(name = str(self.task.id))
        target_group_leader = Group.objects.get(name = "%s%s"%(str(self.task.id), "leaders"))

        # 撤销创建者的相关权限
        creater(user_id = self.task.creater, target_task = self.task).remove_permissions()

        # 撤销组长
        for each in leaders:
            member(user_id = each, target_task = self.task).cancel_leader(target_group = target_group_leader)

        # 组员退出
        for each in members:
            member(user_id = each, target_task = self.task).quit_task(target_group = target_group)

        # 通知

        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

    def task_page(self, request):
        pass

    @staticmethod
    def get_members(request):
        members = UserProfile.objects.filter(major=request.GET.get("key")) | UserProfile.objects.filter(name = request.GET.get("key"))
        members = members.values("name", "major", "user_id", "involved_projects_number", "managed_projects_number")
        
        return JsonResponse(list(members), safe=False)

class _publisher(object):
    detail = None

    def __init__(self, detail):
        self.detail = json.loads(detail)

    def upgrade(self, content, editor_id = 0):
        lastest = self.detail.pop()
        lastest["upgrade_date"] = str(time.time())
        lastest["content"] = content
        lastest["creater"] = editor_id
        self.detail.append(lastest)

        return json.dumps(self.detail)

    def create(self, content, editor_id = 0):
        self.detail.append({"publish_date": str(time.time()), "upgrade_date": str(time.time()), "content": content, "creater": editor_id})
        
        return json.dumps(self.detail)
