from django.urls import path
from . import views


urlpatterns = [
    #path('get_all_notifications/', NotiView.get, name='my_notifications'),
    #path('delete_my_read_notifications/', NotiView.delete_my_read_notifications, name='delete_my_read_notifications'),
    #path('send_notification/', NotiView.send_notification, name="send_notification"),
    ##path('get_user_notification/', NotiView.get_user_notification, name="get_user_notification"),
    #path('my_notifications/', NotiView.my_notifications, name="my_notifications")

    path('get_all_notifications/', views.get_all_notifications),
    path('delete_read_notifications/', views.delete_read_notifications),
    path('send_notification/', views.send_notification),
    path('mark_as_read/', views.mark_as_read),
]
