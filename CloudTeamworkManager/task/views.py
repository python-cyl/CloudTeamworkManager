from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission, Group
from guardian.shortcuts import assign_perm, remove_perm
from guardian.decorators import permission_required
from .models import task as models_task
from .forms import task as forms_task
from account.models import UserProfile
import re
import json


# position：0，1，分别对应组员，组长
# 请注意，这个函数不会修改target_user的权限
def remove_user(target_user, target_task, position = 0):
    target_user.involved_projects_number -= 1
    target_user.involved_projects = json.dumps(json.loads(target_user.involved_projects).remove(target_task.id))
    target_user.save()

# position：0，1，2，分别对应组员，组长, 任务创建者
def add_user(target_user, target_group, target_task, position = 0):
    target_user.involved_projects_number += 1
    target_user.involved_projects = json.dumps(json.loads(user.involved_projects).append(target_task.id))
    target_user.save()

    user = User.objects.get(id = target_user.user_id)
    user.groups.add(target_group)

    position == 2 and assign_perm('edit_tasks', target_user, target_task)

# 检查权限
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": forms_task()})

    if request.method == "POST":
        form = forms_task(request.POST)

        if form.is_valid():
            # 赋予创建者编辑任务的权限
            form.instance.all_members = form.instance.members
            form.instance.creator = request.user.id

            target_task = form.save()
            group = Group.objects.create(name=str(target_task.id))
            assign_perm('glance_over_task_details', group, target_task)

            # 配置创建者
            add_user(UserProfile.objects.get(user_id = request.user.id), group, target_task)
            # 配置组员
            for i in json.loads(form.instance.members):
                try:
                    user = UserProfile.objects.get(id = i)
                except UserProfile.DoesNotExist:
                    continue

                add_user(user, group, target_task)

            # 通知组员

            return HttpResponse("200")
        return HttpResponse("出现错误")

# 检查权限
def edit_task(request):
    if request.method == 'GET':
        target_task = models_task.objects.get(id = request.GET.get("task_id"))
        return render(request, "create_task.html", {"form": forms_task(instance = target_task)})

    if request.method == "POST":
        target_task = models_task.objects.get(id = request.POST.get("task_id"))
        form = forms_task(request.POST, instance = target_task)

        if form.is_valid():
            # 计算新增成员和被移除的成员
            past_members = set(json.loads(target_task.members))
            current_members = set(json.loads(request.POST.get("members")))
            removed_members = past_members - current_members
            new_members = current_members - past_members

            # 更新参与过该任务的成员列表
            form.instance.all_members = json.dumps(list(set(json.loads(form.instance.all_members)) + current_members))
            form.save()

            # 获取权限组
            group = Group.objects.get(name=str(target_task.id))

            # 在组中删除该成员，该成员参与过的任务列表更新
            for i in removed_members:
                try:
                    user = UserProfile.objects.get(id = i)
                except UserProfile.DoesNotExist:
                    continue

                remove_user(user, group, target_task)
                User.objects.get(id = user.user_id).groups.remove(group)

                # 通知组员

            # 配置新增组员
            for i in new_members:
                try:
                    user = UserProfile.objects.get(id = i)
                except UserProfile.DoesNotExist:
                    continue

                add_user(user, target_task)

                # 通知组员

            return HttpResponse("200")
        return HttpResponse("出现错误")

# 检查权限
def delete_task(request):
    target_task = models_task.objects.get(id = request.GET.get("task_id"))
    members = json.loads(target_task.members)
    
    # 撤销权限，删除记录
    Group.objects.get(name=str(target_task.id)).delete()
    remove_perm('edit_tasks', request.user, target_task)

    # 组内成员参与任务的个数减一，删除参与该任务的记录
    for each in members:
        try:
            user = UserProfile.objects.get(id = each)
        except UserProfile.DoesNotExist:
            continue
        
        remove_user(user, target_task)

    # 通知组内成员

    return HttpResponse("200")

# 检查权限
def get_members(request):
    members = UserProfile.objects.filter(magor=request.GET.get("key")) | UserProfile.objects.filter(name = request.GET.get("key"))
    members = members.values("name", "magor", "user_id", "involved_projects_number")
    return HttpResponse(json.dumps(list(members)))

# 检查权限
def task_page(request):
    target_task = models_task.objects.get(id = request.GET.get("task_id"))
    return HttpResponse(target_task)

# 检查权限
def upgrade_process(request):
    # 更新项目进度,修改项目进度
    if request.method == "GET":
        target_task = models_task.objects.get(id = request.GET.get("task_id"))
        progress = target_task.task_progress
        return HttpResponse(progress)

    if request.method == "POST":
        if request.POST.get("action") == "upgrade":
            target_task = models_task.objects.get(id = request.POST.get("task_id"))
            target_task.task_progress = "%s|%s"%(target_task.task_progress, request.POST.get("task_progress"))
            target_task = forms_task(target_task)
            if target_task.is_valid():
                target_task.save()
                return HttpResponse('200')
            return HttpResponse('出现了一些错误!')
        elif request.POST.get("action") == "edit":
            target_task = models_task.objects.get(id = request.POST.get("task_id"))
            target_task.task_progress = "%s%s"%(re.match("^.*\|", target_task.task_progress).group(), request.POST.get("task_progress"))
            target_task = forms_task(target_task)
            if target_task.is_valid():
                target_task.save()
                return HttpResponse('200')
            return HttpResponse('出现了一些错误!')
