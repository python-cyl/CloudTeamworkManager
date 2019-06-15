from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required
from .models import task
from .forms import task as form_task
from account.models import UserProfile

# 检查权限
def create_task(request):
    form = form_task()
    pass

# 检查权限
def change_task(request):
    form = form_task()
    pass

# 检查权限
def get_members(request):
    members = list(UserProfile.objects.get(magor = request.GET.get("magor")))
    return HttpResponse(member)

# 检查权限
def search_member(request):
    members = list(UserProfile.objects.get(name = request.GET.get("name")))
    return HttpResponse(members)

# 检查权限
def change_task_status(request):
    task_id = request.POST.get("task_id")
    task.objects.filter(id = task_id).update(task_status = request.POST.get("task_status"))
    return HttpResponse('200')

# 检查权限 和comment库有关
def show_comment(request):
    pass

# 检查权限 和comment库有关
def change_comment(request):
    pass

def task_page(request):
    target_task = task.objects.get(id = request.GET.get("task_id"))
    return HttpResponse(task)

def show_appendixes(request):
    target_task = task.objects.get(id = request.POST.get("task_id"))
    appendixes = target_task["target_task"]
    return HttpResponse(appendixes)

# 检查权限
def upgrade_process(request):
    target_task = task.objects.get(id = request.POST.get("task_id"))
    target_task = form_task(request.POST, instance = target_task)
    if target_task.is_valid():
        target_task.save()
        return HttpResponse('200')
    return HttpResponse('表单有误!')


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
