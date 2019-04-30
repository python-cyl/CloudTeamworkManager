from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page),
    # path('login/submit/', views.login_submit),
    path('register/', views.register_page),
    # path('register/submit/', views.register_submit),
    path('get_password/', views.get_password_page),
    # path('get_password/submit/', views.get_password_submit),
    path('check_username/', views.check_username),
    path('check_phone_number/', views.check_phone_number),
    path('sendmsgcode/', views.sendmsgcode),
    path('space/', views.space_page),
    path('perfect_information/', views.extend_info),
    # path('perfect_information/submit/', views.extend_info_submit),
    # path('change_information/submit/', views.change_info_submit),
    path('change_information/', views.change_info_page),
]
