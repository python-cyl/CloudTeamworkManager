from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('register/submit/', views.register_submit),
    path('login/submit/', views.login_submit),
]
