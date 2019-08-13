from django.urls import path
from .views import NotiView


urlpatterns = [
    path('my_notifications/', NotiView.as_view(), name='my_notifications'),
    path('delete_my_read_notifications/', NotiView.delete_my_read_notifications, name='delete_my_read_notifications'),
    path('send_notification/', NotiView.send_notification, name="send_notification"),
    path('get_user_notification/', NotiView.get_user_notification, name="get_user_notification"),
    path('my_notifications/', NotiView.my_notifications, name="my_notifications")
]

