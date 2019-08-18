from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic.base import View
from django.urls import reverse
from django.contrib.auth.models import User
import json
import datetime
from notifications.signals import notify
from notifications.models import Notification
from account.models import UserProfile
from django.core import serializers


def delete_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return render(request, 'notifications.html')

def send_notification(request):
    actor = request.user
    type = Notification.objects
    notify.send(actor, recipient=actor, verb='你好鸭，这是标题', description = "这是正文")
    return HttpResponse("ok")

def get_all_notifications(request):
    re = request.user.notifications.all().values('recipient', 'actor_content_type', 'verb', 'description', 'timestamp')
    return JsonResponse(list(re), safe=False)

def mark_as_read(request, notification_id):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    return HttpResponse("ok")

#class ComplexEncoder(json.JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, datetime.datetime):
#            return obj.strftime('%Y-%m-%d %H:%M:%S')
#        else:
#            return json.JSONEncoder.default(self, obj)

#class NotiView(View):
#    def delete_my_read_notifications(request):
#        notifications = request.user.notifications.read()
#        notifications.delete()
#        return render(request, 'notifications.html')


#    def my_notifications(my_notification_pk):
#        my_notification = get_object_or_404(Notification, pk=my_notification_pk)
#        my_notification.unread = False
#        my_notification.save()


#    def get(self, request):
#        re = request.user.notifications.all().values('recipient', 'actor_content_type', 'verb', 'description', 'timestamp')
#        # actor_content_type == 7 为站内消息   3 为组内消息
#        #time = request.user.notifications.all().values('timestamp')
#        #new_time = json.dumps(list(time), cls=ComplexEncoder)
#        ## rr = serializers.serialize('json', re)
#        #rr = json.dumps(list(re))
#        return JsonResponse(re)


#    #def get_user_notification(request):
#    #    re = request.user.notifications.all().values('recipient', 'description', 'timestamp')
#    #    rr = json.dumps(re)


#    def send_notification(request):
#        actor = request.user
#        type = Notification.objects
#        notify.send(actor, recipient=actor, verb='你好鸭')
#        return HttpResponse("ok")
