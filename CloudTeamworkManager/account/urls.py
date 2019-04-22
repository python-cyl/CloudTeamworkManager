from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page),
    path('login/submit/', views.login_submit),
    path('register/', views.register_page),
    path('register/submit/', views.register_submit),
    path('get_password/', views.get_password_page),
    path('get_password/submit/', views.get_password_submit),
    path('space/', views.space_page),
    path('perfect_infomation/submit/', views.extend_info_submit),
]
