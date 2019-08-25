from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from notifications.signals import notify
from notifications.models import Notification


# 类型定义: 1是系统消息，2是组内消息
def delete_all_read(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

def delete_target(request, notification_id):
    notification = Notification.objects.filter(id = notification_id)
    notification.delete()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

def get_read(request):
    notifications = request.user.notifications.read()
    notifications = notifications.values('id', 'actor_content_type', 'verb', 'description', 'timestamp')
    return JsonResponse(list(notifications), safe=False)

def get_unread(request):
    notifications = request.user.notifications.unread()
    notifications = notifications.values('id', 'actor_content_type', 'verb', 'description', 'timestamp')
    return JsonResponse(list(notifications), safe=False)

def mark_all_as_read(request):
    request.user.notifications.unread().mark_all_as_read()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

def mark_target_as_read(request, notification_id):
    notification = Notification.objects.get(id = notification_id)
    notification.mark_as_read()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

def get_target_type(request, type):
    unread = request.user.notifications.unread()
    read = request.user.notifications.read()

    unread = unread.get(actor_content_type = type)
    read = read.get(actor_content_type = type)

    unread = list(unread.values('id', 'actor_content_type', 'verb', 'description', 'timestamp'))
    read = list(read.values('id', 'actor_content_type', 'verb', 'description', 'timestamp'))

    return JsonResponse({"content": {"unread": unread, "read": read}, "status": 200}, safe=False)

def notifications(request):
    readjs = list(request.user.notifications.read().values('recipient', 'data', 'verb', 'description', 'timestamp','id'))
    for i in readjs:
        i['timestamp'] = str(i['timestamp'])[:-7]
    unreadjs = list(request.user.notifications.unread().values('recipient', 'data', 'verb', 'description', 'timestamp','id',))
    for i in unreadjs:
        i['timestamp'] = str(i['timestamp'])[:-7]
    return render(request,'notification.html',{"readjs":json.dumps(readjs),"unreadjs":json.dumps(unreadjs),})

def send_test(request):
    actor = request.user
    type = Notification.objects
    notify.send(actor, recipient=actor, verb='你好鸭，这是测试通知', description = "这是的是通知的正文部分", msg_type=1)
    return HttpResponse("ok")

def get_target_type(request, type): # 1系统 2组内
    unread = request.user.notifications.unread()
    read = request.user.notifications.read()

    unread = unread.filter(data={"type": type})
    read = read.filter(data={"type": type})

    unread = list(unread.values('id', 'data', 'verb', 'description', 'timestamp'))
    read = list(read.values('id', 'data', 'verb', 'description', 'timestamp'))

    return JsonResponse({"content": {"unread": unread, "read": read}, "status": 200}, safe=False)
