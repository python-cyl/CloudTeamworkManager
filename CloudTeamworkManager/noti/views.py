from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from notifications.signals import notify
from notifications.models import Notification


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
    notifications = notifications.values('recipient', 'actor_content_type', 'verb', 'description', 'timestamp')
    return JsonResponse(list(notifications), safe=False)

def get_unread(request):
    notifications = request.user.notifications.unread()
    notifications = notifications.values('recipient', 'actor_content_type', 'verb', 'description', 'timestamp')
    return JsonResponse(list(notifications), safe=False)

def mark_all_as_read(request):
    request.user.notifications.unread().mark_all_as_read()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

def mark_target_as_read(request, notification_id):
    notification = Notification.objects.get(id = notification_id)
    notification.mark_as_read()
    return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

def send_test(request):
    actor = request.user
    type = Notification.objects
    notify.send(actor, recipient=actor, verb='你好鸭，这是测试通知', description = "这是的是通知的正文部分")
    return HttpResponse("ok")
