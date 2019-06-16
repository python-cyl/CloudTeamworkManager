from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required
from .models import task
from .forms import task as form_task
from account.models import UserProfile
import re
import json

def delete_task(request):
    task.objects.get(id = request.GET.get("task_id")).delete()
    return HttpResponse("200")

# 检查权限
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": form_task()})

    if request.method == "POST":
        form = form_task(request.POST)

        if form.is_valid():
            # 给创建者赋予权限
            form.instance.all_members = form.instance.members
            form.save()
            # 通知新增的同学
            for i in json.loads(form.instance.members):
                user = UserProfile.objects.get(id = i)
                user.involved_projects_number += 1
                user.save()
            return HttpResponse("200")
        return HttpResponse("出现错误")

# 检查权限
def edit_task(request):
    if request.method == 'GET':
        target_task = task.objects.get(id = request.GET.get("task_id"))
        return render(request, "create_task.html", {"form": form_task(instance = target_task)})

    if request.method == "POST":
        target_task = task.objects.get(id = request.POST.get("task_id"))
        form = form_task(request.POST, instance = target_task)

        if form.is_valid():
            past_members = set(json.loads(target_task.members))
            current_members = set(json.loads(request.POST.get("members")))
            removed_members = past_members - current_members
            new_members = current_members - past_members
            form.instance.all_members = json.dumps(list(set(json.loads(form.instance.all_members)) + current_members))
            form.save()

            for i in removed_members:
                user = UserProfile.objects.get(id = i)
                user.involved_projects_number -= 1
                user.save()
                # 这里需要给removed_members发送通知

            for i in new_members:
                user = UserProfile.objects.get(id = i)
                user.involved_projects_number += 1
                user.save()
                # 这里需要给new_members发送通知

            return HttpResponse("200")
        return HttpResponse("出现错误")

# 检查权限
def get_members(request):
    members = UserProfile.objects.filter(magor=request.GET.get("key")) | UserProfile.objects.filter(name = request.GET.get("key"))
    members = members.values("name", "magor", "id", "involved_projects_number")
    return HttpResponse(json.dumps(list(members)))

def task_page(request):
    target_task = task.objects.get(id = request.GET.get("task_id"))
    return HttpResponse(task)

# 检查权限
def upgrade_process(request):
    # 更新项目进度,修改项目进度
    if request.method == "GET":
        target_task = task.objects.get(id = request.GET.get("task_id"))
        progress = target_task.task_progress
        return HttpResponse(progress)

    if request.method == "POST":
        if request.POST.get("action") == "upgrade":
            target_task = task.objects.get(id = request.POST.get("task_id"))
            target_task.task_progress = "%s|%s"%(target_task.task_progress, request.POST.get("task_progress"))
            target_task = form_task(target_task)
            if target_task.is_valid():
                target_task.save()
                return HttpResponse('200')
            return HttpResponse('出现了一些错误!')
        elif request.POST.get("action") == "edit":
            target_task = task.objects.get(id = request.POST.get("task_id"))
            target_task.task_progress = "%s%s"%(re.match("^.*\|", target_task.task_progress).group(), request.POST.get("task_progress"))
            target_task = form_task(target_task)
            if target_task.is_valid():
                target_task.save()
                return HttpResponse('200')
            return HttpResponse('出现了一些错误!')


#@login_required
#def get_permission_page(request):
#    if request.user.has_perm('task.create_tasks'):
#        return HttpResponse("你已经拥有权限")
#    permission = Permission.objects.filter(id=42)
#    request.user.user_permissions.add(permission[0])
#    return HttpResponse("你没有权限")

#def add_tasks_page(request):
#    task1 = task.objects.create(publish_data = '1111-10-11', deadline = '1111-10-11', task_need = "这是第一个任务")
#    task2 = task.objects.create(publish_data = '1111-10-11', deadline = '1111-10-11', task_need = "这是第二个任务")
#    user = User.objects.get(username = request.user.username)
#    assign_perm('create_tasks', user, task1)
#    return HttpResponse("新建成功")

#@permission_required('create_tasks', (task, 'id', "need"))
#def check_permission_page(request, need):
#    return HttpResponse("认证成功")
