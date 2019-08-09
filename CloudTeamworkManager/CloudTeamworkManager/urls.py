"""
CloudTeamworkManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from noti.views import NotiView

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('task/', include('task.urls')),
    path('publisher/', include('publisher.urls')),
    path('file/', include('file.urls')),
    #path('notification/', include('account.urls')),
    #path('task/', include('account.urls')),

    #chenyunlong
    path('notifications /', include('notifications.urls', namespace='notifications')),
    path('my_notifications/', NotiView.as_view(), name='my_notifications'),
    path('delete_my_read_notifications/', NotiView.delete_my_read_notifications, name='delete_my_read_notifications'),
    path('send_notification/', NotiView.send_notification, name="send_notification"),
    path('get_user_notification/', NotiView.get_user_notification, name="get_user_notification"),
    path('my_notifications/', NotiView.my_notifications, name="my_notifications")
]
