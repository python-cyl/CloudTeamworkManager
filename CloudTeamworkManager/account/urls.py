from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('get_password/', views.get_password_page),
    path('check_phone_number/', views.check_phone_number),
    path('sendmsgcode/', views.sendmsgcode),
    path('space/', views.space_page),
    path('perfect_information/', views.perfect_info),
    path('change_information/', views.change_info_page),
]
